# Team OS document publication procedure

This procedure publishes согласованные редакционные изменения Team OS back into
Knowledge Substrate without turning review diffs into formatting noise.

## Core principle

Knowledge Substrate keeps the canonical Markdown file. Team OS is the editorial
workflow surface, not the only reliable raw Markdown source.

Разреши канонический URL/UUID через Core resolve_resource; получи исходный
Markdown и version Task/Note. При недоступном OAuth сообщи о reconnect,
не обращайся к ClickUp или PostgreSQL как запасному пути.

## Inputs

Use these inputs for each publication:

1. Task/Note Team OS с подтверждённой готовностью: workflow Task или явное
   согласование пользователя для Note, без выдуманных статусов выполнения Note.
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
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -RecordId <Team OS record UUID>
```

The script:

- reads the raw Markdown as strict UTF-8;
- sets `descriptive.status: active` in the preview;
- resolves the canonical Markdown file from the MkDocs URL;
- checks `title` and `descriptive.id` against the target file;
- writes a preview to `generated/team-os-publication-preview`;
- prints the expected diff;
- reports a diff gate.

Apply only after review:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -RecordId <Team OS record UUID> -Apply
```

Large diffs are blocked by default. Use this only when the rewrite is expected:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -RecordId <Team OS record UUID> -Apply -AllowLargeDiff
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

- готовность Task/Note Team OS и текущая version подтверждены;
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
