---
name: windows-utf8-guard
description: Diagnose and fix mojibake/encoding issues on Windows in Codex workflows. Use when terminal output shows broken Cyrillic/UTF-8, when PowerShell profile or code page causes garbled text, when Git logs/commits display incorrect symbols, or when a stable UTF-8 setup is needed across machine-level and session-level settings.
---

# Windows UTF-8 Guard

## Goal

Stabilize UTF-8 behavior on Windows so Russian text is readable in terminal output, Git history, and Codex-driven workflows.

## Apply Session-Level Fixes

If the current terminal session is broken, apply:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

Use this as a non-destructive first response before deeper changes.


## Confirmation Rule

After changes, always rerun:

1. The original failing command.
2. A UTF-8 check command (`chcp`, encoding output).
3. One Git command that shows non-ASCII paths or commit text.

Report what changed and what remains constrained by policy/sandbox.
