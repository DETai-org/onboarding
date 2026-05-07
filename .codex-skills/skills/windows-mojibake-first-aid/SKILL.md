---
name: windows-mojibake-first-aid
description: First-response runbook for Windows mojibake in Codex workflows. Use when terminal output shows garbled Cyrillic like `Ð...` or `Р...`, or when PowerShell or Git output looks misencoded; apply a safe session-level UTF-8 reset, rerun the failing command, and report whether the issue persists.
---

# Windows Mojibake First Aid

## Goal

Recover a broken Windows terminal session quickly when Cyrillic or UTF-8 output becomes unreadable.

## Use This Skill When

- terminal output contains `Ð...`, `Р...`, `Ñ...` or other mojibake;
- Git output or commit text became unreadable;
- a fast first response is needed, not a full machine setup.

## Runbook

1. Apply the session-level fix in the current shell:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

2. Re-run the original failing command.
3. Confirm the baseline with:

```powershell
chcp
[Console]::OutputEncoding
git config --global --get i18n.logOutputEncoding
```

4. If the output is still broken after the session reset, state that the issue is beyond first response and may require checking the machine-level baseline already covered by onboarding issue #30.

## Confirmation Rule

Always report:

1. which command was failing;
2. whether the session-level reset changed the output;
3. whether Git/global UTF-8 settings still look aligned;
4. what remains unresolved.
