---
name: windows-utf8-guard
description: Diagnose and fix mojibake/encoding issues on Windows in Codex workflows. Use when terminal output shows broken Cyrillic/UTF-8, when PowerShell profile or code page causes garbled text, when Git logs/commits display incorrect symbols, or when a stable UTF-8 setup is needed across machine-level and session-level settings.
---

# Windows UTF-8 Guard

## Goal

Stabilize UTF-8 behavior on Windows so Russian text is readable in terminal output, Git history, and Codex-driven workflows.

## Quick Workflow

1. Verify current environment in active shell.
2. Apply session-level UTF-8 settings if needed.
3. Verify machine-level prerequisites (PowerShell 7, terminal/code page).
4. Verify Git global encoding settings.
5. Re-run the failed command and confirm the output is readable.

## Step 1. Run Diagnostic Checks

Run:

```powershell
pwsh -v
[Console]::OutputEncoding
chcp
git config --global --get i18n.commitEncoding
git config --global --get i18n.logOutputEncoding
git config --global --get core.quotepath
git config --global --get gui.encoding
```

Treat these as healthy defaults:

- PowerShell 7.x is installed.
- Output encoding is UTF-8.
- Active code page is `65001`.
- Git values are `utf-8` and `core.quotepath=false`.

## Step 2. Apply Session-Level Fixes

If the current terminal session is broken, apply:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

Use this as a non-destructive first response before deeper changes.

## Step 3. Apply Machine-Level Baseline

Install/upgrade PowerShell via `winget`:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

Then configure profile defaults (if profile is allowed by execution policy):

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

If profile loading is blocked, keep using session-level commands and note policy constraints explicitly.

## Step 4. Normalize Git Encoding

Apply once per machine:

```powershell
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8
git config --global core.quotepath false
git config --global gui.encoding utf-8
```

## Step 5. Confirmation Rule

After changes, always rerun:

1. The original failing command.
2. A UTF-8 check command (`chcp`, encoding output).
3. One Git command that shows non-ASCII paths or commit text.

Report what changed and what remains constrained by policy/sandbox.
