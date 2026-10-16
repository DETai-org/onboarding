# Launch the installed Remote MCP with explicit Node proxy support.
# No global environment changes, node_modules patches, logout or new device.
[CmdletBinding()]
param(
    [ValidateSet('Auto','Proxy','Direct')][string]$NetworkMode = 'Auto',
    [switch]$PlanOnly
)
$ErrorActionPreference = 'Stop'
$node = (Get-Command node.exe -ErrorAction Stop).Source
$versionText = (& $node --version).Trim().TrimStart('v')
if ($LASTEXITCODE -ne 0 -or [version]$versionText -lt [version]'24.5.0') {
    throw 'This launcher is tested with Node 24.15; Node 24.5+ is required.'
}
# npm.cmd may emit UTF-8 paths even when Windows PowerShell expects a legacy code page.
# Decode the subprocess output as UTF-8 (e.g. C:\Users\Антон) without changing system settings.
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$globalRoot = (& npm.cmd root -g).Trim()
if ($LASTEXITCODE -ne 0 -or !$globalRoot) { throw 'Cannot locate global npm packages.' }
$packageDir = Join-Path $globalRoot '@wonderwhy-er\desktop-commander'
$manifestPath = Join-Path $packageDir 'package.json'
$entry = Join-Path $packageDir 'dist\index.js'
if (!(Test-Path -LiteralPath $manifestPath) -or !(Test-Path -LiteralPath $entry)) {
    throw 'Desktop Commander is not globally installed. Run: npm install -g @wonderwhy-er/desktop-commander@latest'
}
$manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json
if ($manifest.name -ne '@wonderwhy-er/desktop-commander') { throw 'Unexpected global npm package.' }
$packageVersion = $manifest.version
$settings = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings'
$proxy = $null
if ($NetworkMode -eq 'Proxy' -or ($NetworkMode -eq 'Auto' -and $settings.ProxyEnable -eq 1)) {
    $server = [string]$settings.ProxyServer
    if ($server.Contains('=')) {
        $items = @{}
        foreach ($part in $server.Split(';')) {
            $kv = $part.Split('=',2)
            if ($kv.Count -eq 2) { $items[$kv[0].Trim()] = $kv[1].Trim() }
        }
        $server = if ($items.ContainsKey('https')) { $items['https'] } else { $items['http'] }
    }
    if (!$server) { throw 'Enable the existing Happ system proxy first; no automatic direct fallback.' }
    if ($server -notmatch '^https?://') { $server = 'http://' + $server }
    $uri = [uri]$server
    if (!$uri.IsLoopback -or $uri.UserInfo -or $uri.Scheme -ne 'http') {
        throw 'Expected the existing local HTTP proxy; remote proxies/PAC are not supported by this launcher.'
    }
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $attempt = $client.BeginConnect($uri.Host,$uri.Port,$null,$null)
        if (!$attempt.AsyncWaitHandle.WaitOne(1500)) { throw 'The local proxy is not listening.' }
        $client.EndConnect($attempt)
    } finally { $client.Dispose() }
    $proxy = $uri.GetLeftPart([System.UriPartial]::Authority)
}
$effective = if ($proxy) { "PROXY $proxy" } else { 'DIRECT (use World, or another working direct network)' }
Write-Output "Desktop Commander $packageVersion / Node $versionText / $effective"
if ($PlanOnly) { Write-Output "Entry: $entry"; exit 0 }
$active = @(Get-CimInstance Win32_Process -Filter "name='node.exe'" | Where-Object {
    $_.CommandLine -match '(?i)desktop-commander[\\/]dist[\\/]index\.js.*\bremote\b'
})
if ($active.Count) { throw 'Commander Remote is already running. Stop its terminal with Ctrl+C before starting another copy.' }
$names = @('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','NO_PROXY','NODE_USE_ENV_PROXY')
$saved = @{}
foreach ($name in $names) {
    $saved[$name] = [Environment]::GetEnvironmentVariable($name,'Process')
    [Environment]::SetEnvironmentVariable($name,$null,'Process')
}
try {
    if ($proxy) {
        $env:HTTP_PROXY = $proxy
        $env:HTTPS_PROXY = $proxy
        $env:NO_PROXY = 'localhost,127.0.0.1,::1'
        $env:NODE_USE_ENV_PROXY = '1'
        & $node --use-env-proxy $entry remote
    } else { & $node $entry remote }
    $result = $LASTEXITCODE
} finally {
    foreach ($name in $names) { [Environment]::SetEnvironmentVariable($name,$saved[$name],'Process') }
}
exit $result
