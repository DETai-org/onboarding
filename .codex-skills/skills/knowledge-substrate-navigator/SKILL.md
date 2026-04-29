---
name: knowledge-substrate-navigator
version: 0.1.1
description: Use when the user provides a DETai Knowledge Substrate public MkDocs URL or asks to locate/read canonical Knowledge Substrate documentation from a local clone. Maps public URLs to local source-of-truth Markdown, reads Markdown as strict UTF-8, and ignores repo code/generated folders.
---

# Knowledge Substrate Navigator

## Purpose

Use this skill as a small read-only infrastructure ability for finding and reading canonical DETai Knowledge Substrate documents.

This skill is not a methodology, planning, implementation, release, or documentation-architecture skill. It only answers: "Given a public Knowledge Substrate page or documentation target, where is the canonical local Markdown source and how should it be read safely?"

## Scope

Use this skill when:

- the user provides a `https://detai-org.github.io/Knowledge_substrate/...` URL;
- another skill needs canonical Knowledge Substrate source files;
- local Markdown from Knowledge Substrate must be read without PowerShell mojibake;
- a public MkDocs URL must be mapped to a local source-of-truth file.

Do not use this skill to:

- design Epic Issues, Sub-Issues, Work Packages, releases, or documentation plans;
- analyze implementation code in the Knowledge_substrate repository;
- broadly crawl the whole repository unless the user asks for broad discovery;
- mutate, normalize, re-encode, or rewrite Knowledge Substrate files.

## Local Repository Discovery

Prefer local source files over rendered public pages.

Common local clone shapes:

- `D:\dev\DETai-org\Knowledge_substrate`
- the current workspace, when it contains `knowledge_core/source_of_truth/docs`

Treat `D:\dev\DETai-org\Knowledge_substrate` as the primary local clone path on the shared workstation.

The documentation root is:

```text
knowledge_core/source_of_truth/docs
```

Only search documentation roots by default. Ignore:

```text
.git/
site/
node_modules/
.venv/
__pycache__/
cache/
logs/
generated/
detai-core/
```

## URL To Markdown Mapping

For a public URL like:

```text
https://detai-org.github.io/Knowledge_substrate/ru/ecosystem/Management_layer/2_Architecture_and_Logic/Versioning-process/
```

map the URL path after `/Knowledge_substrate/` into the docs root:

```text
knowledge_core/source_of_truth/docs/ru/ecosystem/Management_layer/2_Architecture_and_Logic/Versioning-process.md
```

Also check these fallbacks:

```text
.../<slug>/index.md
.../<slug>.md
```

If direct mapping fails, search Markdown frontmatter for:

```yaml
links:
  external_links:
    - type: "MkDocs_ru"
      url: "<public URL>"
```

Normalize trailing slashes before comparing public URLs.

## UTF-8 Reading Rule

On Windows/PowerShell, do not trust console-rendered Russian text until strict UTF-8 byte decoding has been checked.

Preferred read pattern:

```powershell
$utf8 = [Text.UTF8Encoding]::new($false, $true)
$text = $utf8.GetString([IO.File]::ReadAllBytes($path))
```

If using `Get-Content`, set output encoding first:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -Encoding UTF8 -LiteralPath $path
```

If text appears as `Рџ...`, `вЂ...`, or `пёЏ...`, verify with strict UTF-8 byte decoding before concluding the file is corrupted.

## Fallback To Public Pages

If no local source file is available, read the public URL through direct HTTP/web-reading capability.

Use Browser Use / browser only for visual layout, screenshots, JavaScript-only state, or interactive navigation. Do not use a browser just to read Markdown content.

## Reporting

When this skill is used, report:

- public URL received;
- local Markdown path found, if any;
- whether strict UTF-8 decoding succeeded;
- if local source was unavailable, which public source was used instead.
