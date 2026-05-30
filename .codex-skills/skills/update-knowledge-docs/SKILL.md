---
name: update-knowledge-docs
description: Publish edited Knowledge Substrate Markdown documents from the ClickUp "Новые версии документов" workflow back into the canonical Knowledge_substrate repository. Use when Codex needs to take a ClickUp task with status READY FOR PUBLICATION, prepare or verify raw Markdown, preserve reviewable Git diffs, run dry-run/apply publication checks, and create a PR-ready document update.
---

# Update Knowledge Docs

Use this skill for the reverse publication flow:

```text
ClickUp READY FOR PUBLICATION -> raw Markdown source -> Knowledge Substrate Markdown -> Git branch / PR
```

The goal is not only to publish text, but to keep the GitHub diff reviewable.
If one paragraph changed, the PR should show that paragraph plus required
metadata changes, not a whole-document formatting rewrite.

## Core Rules

- Treat Knowledge Substrate as the canonical Markdown source.
- Treat ClickUp as editorial workflow/status context, not as the only reliable
  raw Markdown store.
- Do not publish ClickUp connector `description` directly when it has been
  normalized to plain text.
- Start publication sources from the current canonical Markdown or generated
  baseline Markdown, then apply the ready task's editorial changes.
- Preserve existing Markdown formatting unless formatting normalization is an
  explicit editorial change.
- Keep formatting normalization in a separate PR from document publication.

## Required Context

Before applying a publication, gather:

1. ClickUp task id or URL for the ready task.
2. Ready task status, which must be `ready for publication`.
3. Matching baseline task or current canonical Markdown file.
4. Raw Markdown publication source.
5. Canonical Knowledge Substrate file path.

For detailed preparation rules, read:

```text
references/raw-markdown-source-checklist.md
```

For the full end-to-end procedure, read:

```text
references/clickup-doc-publication-procedure.md
```

## Script

Use the bundled script:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -TaskId <ClickUp task id>
```

The script:

- reads the raw Markdown as strict UTF-8;
- sets `descriptive.status: active` in preview/apply output;
- resolves the canonical Markdown file from the MkDocs URL;
- checks `title` and `descriptive.id` against the target file;
- writes a preview into `generated/clickup-publication-preview`;
- reports `diff_gate`;
- blocks large apply diffs unless `-AllowLargeDiff` is explicit.

Apply only after reviewing dry-run output:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -TaskId <ClickUp task id> -Apply
```

Use this only for intentional major rewrites:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -TaskId <ClickUp task id> -Apply -AllowLargeDiff
```

## Manual Checks

Before `-Apply`, verify:

- ClickUp task status is `ready for publication`.
- Task title matches front matter `title`.
- `descriptive.id` matches the existing canonical target file.
- `classification.scope`, `classification.function`, and title changes are
  intentional.
- `descriptive.version` is the expected new version.
- Preview has `descriptive.status: active`.
- `diff_gate.status` is `ok`, or `large-diff` is justified by a real major
  rewrite.
- Git diff is readable by a human reviewer.

After `-Apply`, run:

```powershell
git diff --check
git diff --stat
git diff -- <canonical file>
```

Also verify strict UTF-8, no BOM, and LF line endings.

## PR Policy

While calibrating this workflow, prefer one document per PR.

Do not mix:

- publication changes;
- Markdown normalization;
- script or skill edits;
- unrelated status updates.

If a draft PR accidentally includes extra commits/files, close it and recreate
a clean PR from `origin/main` with only the intended document publication.

Every document-publication PR should have the GitHub label
`update-knowledge-docs`. Use the GitHub API or connector to add it when opening
or updating the PR.

For a lightweight example of the expected PR shape, use:

```text
https://github.com/DETai-org/Knowledge_substrate/pull/207
```
