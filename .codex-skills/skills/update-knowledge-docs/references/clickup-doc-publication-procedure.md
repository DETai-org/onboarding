# ClickUp document publication procedure

This procedure publishes edited ClickUp document versions back into
Knowledge Substrate without turning review diffs into formatting noise.

## Core principle

Knowledge Substrate keeps the canonical Markdown file. ClickUp is the editorial
workflow surface, not the only reliable raw Markdown source.

The ClickUp connector may return task descriptions as normalized plain text.
Do not publish that text directly into Knowledge Substrate unless the document
is intentionally being reconstructed.

## Inputs

Use these inputs for each publication:

1. ClickUp task in `READY FOR PUBLICATION`.
2. Matching `BASELINE` task or current canonical Markdown file.
3. Raw Markdown publication source in `Management_Layer/generated/...`.
4. Canonical Knowledge Substrate Markdown file resolved from front matter
   `links.external_links` or `descriptive.id`.

## Raw Markdown rule

The publication source should be baseline-preserving:

- start from the current canonical Markdown or generated baseline Markdown;
- apply only the editorial changes from the ready task;
- keep existing headings, blank lines, list style, code fence style, table style,
  and trailing line-break style unless changing them is part of the editorial
  decision;
- never normalize the whole document during publication just because the source
  looks untidy.

If a document needs formatting normalization, do it in a separate PR.

## Script workflow

Dry-run first:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -TaskId <ClickUp task id>
```

The script:

- reads the raw Markdown as strict UTF-8;
- sets `descriptive.status: active` in the preview;
- resolves the canonical Markdown file from the MkDocs URL;
- checks `title` and `descriptive.id` against the target file;
- writes a preview to `generated/clickup-publication-preview`;
- prints the expected diff;
- reports a diff gate.

Apply only after review:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -TaskId <ClickUp task id> -Apply
```

Large diffs are blocked by default. Use this only when the rewrite is expected:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -TaskId <ClickUp task id> -Apply -AllowLargeDiff
```

## Diff gate interpretation

`status: ok` means the diff is small enough for ordinary publication.

`status: large-diff` means one of these is true:

- changed lines are above `MaxChangedLines`;
- changed ratio is above `MaxChangedRatio`;
- the diff may include formatting churn.

For `large-diff`, do not apply immediately. First decide which case it is:

- real major new version: acceptable, use `-AllowLargeDiff` after manual review;
- accidental Markdown normalization: rebuild the raw Markdown source from the
  baseline and preserve formatting;
- wrong target file: stop and fix the source metadata or MkDocs URL.

## Manual checks

Before applying:

- ClickUp task status is `ready for publication`;
- task title matches front matter `title`;
- ready task version matches front matter `descriptive.version`;
- canonical path is the existing file, not a new path;
- `descriptive.status` in the publication preview is `active`;
- `title`, `classification.scope`, `classification.function`, and
  `descriptive.id` are unchanged unless intentionally changed;
- links point to current canonical MkDocs URLs;
- GitHub diff is reviewable.

After applying:

```powershell
git diff --check
git diff --stat
git diff -- <canonical file>
```

Also verify strict UTF-8, no BOM, and LF line endings.

## PR policy

Use small PRs while this workflow is still being calibrated.

For the first batch, prefer one document per PR. After the procedure proves
stable, group related documents only when each diff remains readable.

Do not mix publication changes with Markdown normalization, script work, or
unrelated status updates.

Add the GitHub label `update-knowledge-docs` to every PR created by this
workflow. This makes it possible to review the documentation-publication history
later, independent of code and infrastructure changes in the same repository.

If an example PR is useful, use this one as the reference shape:

```text
https://github.com/DETai-org/Knowledge_substrate/pull/207
```
