---
name: update-knowledge-docs
description: Публикует согласованные редакционные изменения из Task/Note Team OS в канонический репозиторий Knowledge_substrate. Используй для подготовки raw Markdown, проверки готовности к публикации, dry-run/apply и reviewable Git PR с сохранением форматирования.
---

# Update Knowledge Docs

Use this skill for the reverse publication flow:

```text
Team OS Task/Note -> согласованный raw Markdown -> Knowledge Substrate Markdown -> Git branch / PR
```

The goal is not only to publish text, but to keep the GitHub diff reviewable.
If one paragraph changed, the PR should show that paragraph plus required
metadata changes, not a whole-document formatting rewrite.

## Core Rules

- Treat Knowledge Substrate as the canonical Markdown source.
- Редакционный контекст хранится в Team OS. Разреши Team OS URL/UUID через
  resolve_resource и прочитай исходный Markdown и version канонической Task/Note.
  Тип и проект подтверждает Core; новый источник не требует ClickUp provenance.
- Используй исходный descriptionMd/bodyMd, а не визуальный plain-text пересказ.
  Если MCP требует reconnect или доступ закрыт, сообщи о недостающем подключении;
  не возвращайся в ClickUp, не угадывай UUID и не обходи Core через БД.
- Start publication sources from the current canonical Markdown or generated
  baseline Markdown, then apply the ready task's editorial changes.
- Preserve existing Markdown formatting unless formatting normalization is an
  explicit editorial change.
- Keep formatting normalization in a separate PR from document publication.

## Required Context

Before applying a publication, gather:

1. Канонический UUID/URL Task или Note Team OS и текущая version.
2. Для Task — workflow готовности к публикации; для Note — явное согласование
   пользователя. Не добавляй Note статусы выполнения Task.
3. Matching baseline task or current canonical Markdown file.
4. Raw Markdown publication source.
5. Canonical Knowledge Substrate file path.

For detailed preparation rules, read:

```text
references/raw-markdown-source-checklist.md
```

For the full end-to-end procedure, read:

```text
references/team-os-doc-publication-procedure.md
```

## Script

Имя publish-clickup-doc-version.ps1 сохранено для совместимости старых callers.
Скрипт обрабатывает локальный Markdown и не обращается к ClickUp; RecordId —
канонический UUID Team OS.

Use the bundled script:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -RecordId <Team OS record UUID>
```

The script:

- reads the raw Markdown as strict UTF-8;
- sets `descriptive.status: active` in preview/apply output;
- resolves the canonical Markdown file from the MkDocs URL;
- checks `title` and `descriptive.id` against the target file;
- writes a preview into `generated/team-os-publication-preview`;
- reports `diff_gate`;
- blocks large apply diffs unless `-AllowLargeDiff` is explicit.

Apply only after reviewing dry-run output:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -RecordId <Team OS record UUID> -Apply
```

Use this only for intentional major rewrites:

```powershell
.\scripts\publish-clickup-doc-version.ps1 <raw markdown source> -RecordId <Team OS record UUID> -Apply -AllowLargeDiff
```

## Manual Checks

Before `-Apply`, verify:

- Готовность источника Team OS подтверждена по текущей version: workflow Task
  или явное согласование Note.
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
