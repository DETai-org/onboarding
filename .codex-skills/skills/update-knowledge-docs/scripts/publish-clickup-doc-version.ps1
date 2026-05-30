<#
.SYNOPSIS
Publish a prepared ClickUp document version back into Knowledge Substrate.

.DESCRIPTION
This script is the reverse side of export-knowledge-doc-to-clickup-new-version.ps1.
It intentionally treats ClickUp as workflow/status metadata and prefers a local
raw Markdown source for the actual document body, because ClickUp rich text may
normalize Markdown when descriptions are read back through API/connectors.

Default mode is dry-run: it validates inputs, resolves the canonical Markdown
file from front matter, writes a preview, and prints the expected git diff.
Use -Apply to overwrite the canonical Knowledge Substrate Markdown file.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$MarkdownSource,

    [string]$TaskId,

    [string]$KnowledgeRoot = "D:\dev\DETai-org\Knowledge_substrate",

    [string]$DocsRoot = "knowledge_core\source_of_truth\docs",

    [string]$OutputDir = "D:\dev\DETai-org\Management_Layer\generated\clickup-publication-preview",

    [int]$MaxChangedLines = 40,

    [double]$MaxChangedRatio = 0.35,

    [switch]$AllowLargeDiff,

    [switch]$Apply
)

$ErrorActionPreference = "Stop"

function Read-StrictUtf8 {
    param([Parameter(Mandatory = $true)][string]$Path)

    $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
    return $utf8.GetString([System.IO.File]::ReadAllBytes($Path))
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Text
    )

    $utf8 = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText($Path, $Text, $utf8)
}

function Resolve-InputFile {
    param([Parameter(Mandatory = $true)][string]$Path)

    if ([System.IO.File]::Exists($Path)) {
        return (Resolve-Path -LiteralPath $Path).Path
    }

    throw "Markdown source not found: $Path"
}

function Get-FrontMatter {
    param([Parameter(Mandatory = $true)][string]$Text)

    $match = [regex]::Match($Text, '(?s)\A---\r?\n(?<yaml>.*?)\r?\n---\r?\n?')
    if (-not $match.Success) {
        throw "Document does not start with YAML front matter."
    }

    return @{
        FullMatch = $match.Value
        Yaml = $match.Groups["yaml"].Value
        BodyStart = $match.Length
    }
}

function Get-YamlScalar {
    param(
        [Parameter(Mandatory = $true)][string]$Yaml,
        [Parameter(Mandatory = $true)][string]$Key,
        [string]$Section
    )

    $lines = $Yaml -split "\r?\n"
    $inSection = [string]::IsNullOrWhiteSpace($Section)

    foreach ($line in $lines) {
        if (-not [string]::IsNullOrWhiteSpace($Section) -and $line -match "^$([regex]::Escape($Section)):\s*$") {
            $inSection = $true
            continue
        }

        if (-not [string]::IsNullOrWhiteSpace($Section) -and $line -match '^\S' -and $line -notmatch "^$([regex]::Escape($Section)):\s*$") {
            $inSection = $false
        }

        if ($inSection -and $line -match "^\s*$([regex]::Escape($Key)):\s*(.+?)\s*$") {
            return ($Matches[1].Trim().Trim('"').Trim("'"))
        }
    }

    return $null
}

function Get-MkDocsUrl {
    param([Parameter(Mandatory = $true)][string]$Yaml)

    $match = [regex]::Match($Yaml, 'url:\s*"(?<url>https://detai-org\.github\.io/Knowledge_substrate/[^"]+)"')
    if ($match.Success) {
        return $match.Groups["url"].Value
    }

    $match = [regex]::Match($Yaml, "url:\s*'(?<url>https://detai-org\.github\.io/Knowledge_substrate/[^']+)'")
    if ($match.Success) {
        return $match.Groups["url"].Value
    }

    $match = [regex]::Match($Yaml, 'url:\s*(?<url>https://detai-org\.github\.io/Knowledge_substrate/\S+)')
    if ($match.Success) {
        return $match.Groups["url"].Value.Trim()
    }

    return $null
}

function Resolve-KnowledgeMarkdownPathFromUrl {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$RelativeDocsRoot
    )

    if ($Url -notmatch '^https://detai-org\.github\.io/Knowledge_substrate/(.+?)/?$') {
        throw "Unsupported MkDocs URL: $Url"
    }

    $relativeUrl = [System.Uri]::UnescapeDataString($Matches[1])
    $docsPath = Join-Path $Root $RelativeDocsRoot
    $candidate = Join-Path $docsPath ($relativeUrl -replace '/', '\')

    $candidates = @(
        "$candidate.md",
        (Join-Path $candidate "index.md")
    )

    foreach ($path in $candidates) {
        if ([System.IO.File]::Exists($path)) {
            return (Resolve-Path -LiteralPath $path).Path
        }
    }

    throw "Could not map MkDocs URL to Markdown source: $Url"
}

function Set-DescriptiveStatusActive {
    param([Parameter(Mandatory = $true)][string]$Text)

    $frontMatter = Get-FrontMatter -Text $Text
    $yaml = $frontMatter.Yaml
    $lines = $yaml -split "(\r?\n)"
    $rebuilt = New-Object System.Text.StringBuilder
    $inDescriptive = $false
    $changed = $false

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]

        if ($line -match '^descriptive:\s*$') {
            $inDescriptive = $true
        } elseif ($line -match '^\S' -and $line -notmatch '^descriptive:\s*$') {
            $inDescriptive = $false
        }

        if ($inDescriptive -and $line -match '^(\s*)status:\s*(.+?)\s*$') {
            [void]$rebuilt.Append("$($Matches[1])status: active")
            $changed = $true
        } else {
            [void]$rebuilt.Append($line)
        }
    }

    if (-not $changed) {
        throw "Could not find descriptive.status in front matter."
    }

    $body = $Text.Substring($frontMatter.BodyStart)
    return "---`n$($rebuilt.ToString())`n---`n" + $body
}

function Convert-ToSafeFileName {
    param([Parameter(Mandatory = $true)][string]$Text)

    $safe = $Text -replace '[^\p{L}\p{Nd}\-_. ]', ''
    $safe = $safe.Trim() -replace '\s+', '-'
    if ([string]::IsNullOrWhiteSpace($safe)) {
        return "document"
    }
    return $safe
}

function Invoke-GitDiffNoIndex {
    param(
        [Parameter(Mandatory = $true)][string]$OldPath,
        [Parameter(Mandatory = $true)][string]$NewPath,
        [Parameter(Mandatory = $true)][string]$Root
    )

    $oldRelative = Resolve-Path -LiteralPath $OldPath -Relative
    $newRelative = Resolve-Path -LiteralPath $NewPath -Relative
    Push-Location $Root
    try {
        git diff --no-index -- $oldRelative $newRelative
        if ($LASTEXITCODE -gt 1) {
            throw "git diff --no-index failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }
}

function Get-LineCount {
    param([Parameter(Mandatory = $true)][string]$Text)

    if ($Text.Length -eq 0) {
        return 0
    }

    return (($Text -split "\r?\n").Count)
}

function Get-GitNoIndexNumstat {
    param(
        [Parameter(Mandatory = $true)][string]$OldPath,
        [Parameter(Mandatory = $true)][string]$NewPath,
        [Parameter(Mandatory = $true)][string]$Root,
        [switch]$IgnoreWhitespaceNoise
    )

    Push-Location $Root
    try {
        $args = @("diff", "--no-index", "--numstat")
        if ($IgnoreWhitespaceNoise) {
            $args += @("--ignore-space-at-eol", "--ignore-blank-lines")
        }
        $args += @("--", $OldPath, $NewPath)

        $output = & git @args
        $exitCode = $LASTEXITCODE
        if ($exitCode -gt 1) {
            throw "git diff --no-index --numstat failed with exit code $exitCode"
        }
    } finally {
        Pop-Location
    }

    $added = 0
    $deleted = 0

    foreach ($line in $output) {
        $parts = $line -split "`t"
        if ($parts.Count -lt 3) {
            continue
        }

        if ($parts[0] -match '^\d+$') {
            $added += [int]$parts[0]
        }
        if ($parts[1] -match '^\d+$') {
            $deleted += [int]$parts[1]
        }
    }

    return @{
        Added = $added
        Deleted = $deleted
        Changed = $added + $deleted
    }
}

function Get-DiffGate {
    param(
        [Parameter(Mandatory = $true)][string]$OldPath,
        [Parameter(Mandatory = $true)][string]$NewPath,
        [Parameter(Mandatory = $true)][string]$OldText,
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][int]$ChangedLinesLimit,
        [Parameter(Mandatory = $true)][double]$ChangedRatioLimit
    )

    $lineCount = [Math]::Max((Get-LineCount -Text $OldText), 1)
    $numstat = Get-GitNoIndexNumstat -OldPath $OldPath -NewPath $NewPath -Root $Root
    $stableNumstat = Get-GitNoIndexNumstat -OldPath $OldPath -NewPath $NewPath -Root $Root -IgnoreWhitespaceNoise
    $ratio = [Math]::Round(($numstat.Changed / $lineCount), 4)
    $stableRatio = [Math]::Round(($stableNumstat.Changed / $lineCount), 4)
    $isLarge = ($numstat.Changed -gt $ChangedLinesLimit) -or ($ratio -gt $ChangedRatioLimit)
    $formattingNoiseLines = [Math]::Max(($numstat.Changed - $stableNumstat.Changed), 0)
    $hasFormattingNoise = $formattingNoiseLines -ge 10

    $status = "ok"
    $reason = "Diff is within publication limits."
    if ($isLarge) {
        $status = "large-diff"
        $reason = "Diff changes $($numstat.Changed) lines ($ratio of the current file), which is above the configured gate."
    }
    if ($hasFormattingNoise) {
        $reason = "$reason Whitespace/blank-line-insensitive diff is $($stableNumstat.Changed) lines, suggesting formatting churn may be present."
    }

    return [ordered]@{
        status = $status
        reason = $reason
        added_lines = $numstat.Added
        deleted_lines = $numstat.Deleted
        changed_lines = $numstat.Changed
        current_line_count = $lineCount
        changed_ratio = $ratio
        stable_changed_lines = $stableNumstat.Changed
        stable_changed_ratio = $stableRatio
        formatting_noise_lines = $formattingNoiseLines
        max_changed_lines = $ChangedLinesLimit
        max_changed_ratio = $ChangedRatioLimit
    }
}

$sourcePath = Resolve-InputFile -Path $MarkdownSource
$sourceText = Read-StrictUtf8 -Path $sourcePath
$publishText = Set-DescriptiveStatusActive -Text $sourceText
$publishFrontMatter = Get-FrontMatter -Text $publishText

$title = Get-YamlScalar -Yaml $publishFrontMatter.Yaml -Key "title"
$scope = Get-YamlScalar -Yaml $publishFrontMatter.Yaml -Section "classification" -Key "scope"
$function = Get-YamlScalar -Yaml $publishFrontMatter.Yaml -Section "classification" -Key "function"
$version = Get-YamlScalar -Yaml $publishFrontMatter.Yaml -Section "descriptive" -Key "version"
$status = Get-YamlScalar -Yaml $publishFrontMatter.Yaml -Section "descriptive" -Key "status"
$docId = Get-YamlScalar -Yaml $publishFrontMatter.Yaml -Section "descriptive" -Key "id"
$mkdocsUrl = Get-MkDocsUrl -Yaml $publishFrontMatter.Yaml

if ([string]::IsNullOrWhiteSpace($title)) {
    throw "Could not extract title from front matter."
}
if ([string]::IsNullOrWhiteSpace($docId)) {
    throw "Could not extract descriptive.id from front matter."
}
if ($status -ne "active") {
    throw "Internal error: generated document status is not active."
}
if ([string]::IsNullOrWhiteSpace($mkdocsUrl)) {
    throw "Could not extract MkDocs external link from front matter."
}

$targetPath = Resolve-KnowledgeMarkdownPathFromUrl -Url $mkdocsUrl -Root $KnowledgeRoot -RelativeDocsRoot $DocsRoot
$currentText = Read-StrictUtf8 -Path $targetPath
$currentFrontMatter = Get-FrontMatter -Text $currentText
$currentTitle = Get-YamlScalar -Yaml $currentFrontMatter.Yaml -Key "title"
$currentDocId = Get-YamlScalar -Yaml $currentFrontMatter.Yaml -Section "descriptive" -Key "id"

if ($currentDocId -ne $docId) {
    throw "Document id mismatch. Source has '$docId', target has '$currentDocId'."
}
if ($currentTitle -ne $title) {
    throw "Title mismatch. Source has '$title', target has '$currentTitle'."
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$slug = Convert-ToSafeFileName -Text $title
$previewPath = Join-Path $OutputDir "$slug.publish-preview.md"
Write-Utf8NoBom -Path $previewPath -Text $publishText

$diffGate = Get-DiffGate `
    -OldPath $targetPath `
    -NewPath $previewPath `
    -OldText $currentText `
    -Root $KnowledgeRoot `
    -ChangedLinesLimit $MaxChangedLines `
    -ChangedRatioLimit $MaxChangedRatio

if ($Apply -and $diffGate.status -ne "ok" -and -not $AllowLargeDiff) {
    throw "Refusing to apply publication because diff gate is '$($diffGate.status)'. $($diffGate.reason) Review the preview and rerun with -AllowLargeDiff only when the rewrite is intentional."
}

if ($Apply) {
    Write-Utf8NoBom -Path $targetPath -Text $publishText
}

$result = [ordered]@{
    mode = $(if ($Apply) { "apply" } else { "dry-run" })
    task_id = $TaskId
    markdown_source = $sourcePath
    canonical_path = $targetPath
    preview_path = $previewPath
    title = $title
    descriptive_id = $docId
    scope = $scope
    function = $function
    version = $version
    status = $status
    mkdocs_url = $mkdocsUrl
    diff_gate = $diffGate
    allow_large_diff = [bool]$AllowLargeDiff
    note = "Dry-run writes preview only. Apply is blocked for large diffs unless -AllowLargeDiff is set."
}

$result | ConvertTo-Json -Depth 10

if (-not $Apply) {
    Invoke-GitDiffNoIndex -OldPath $targetPath -NewPath $previewPath -Root $KnowledgeRoot
}
