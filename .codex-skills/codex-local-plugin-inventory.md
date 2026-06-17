# Local Codex Plugin Inventory

Снимок локальной технической папки Codex:

```text
C:\Users\PC\.codex\plugins\cache
```

Дата сверки: `2026-06-17`.

Этот файл не является установщиком plugins. Он фиксирует, какие Codex plugins реально есть в локальном cache на рабочей машине, и помогает понять, какие cached copies выглядят legacy по сравнению с текущими remote/runtime копиями.

## Активные И Актуальные Cache Copies

| Plugin | Cache family | Version | Назначение |
| --- | --- | --- | --- |
| `airtable` | `openai-curated-remote` | `0.1.2` | Работа с Airtable как операционной базой: bases, records, tables, поля и совместная структура данных. |
| `browser` | `openai-bundled` | `26.609.41114` | Управление in-app Browser Codex для локальных web targets, screenshots, кликов, форм и визуальной проверки. |
| `canva` | `openai-curated-remote` | `1.0.2` | Поиск, создание, редактирование и адаптация Canva designs. |
| `clickup` | `openai-curated-remote` | `1.0.2` | Операционная работа с ClickUp: задачи, документы, списки, проекты и workflow-состояния. |
| `computer-use` | `openai-bundled` | `26.609.41114` | Управление Windows desktop apps из Codex. |
| `documents` | `openai-primary-runtime` | `26.614.11602` | Создание, редактирование и проверка Word / `.docx` документов. |
| `figma` | `openai-curated-remote` | `2.0.9` | Работа с Figma: дизайн, design systems, Code Connect и перенос UI в Figma. |
| `github` | `openai-curated-remote` | `0.1.2` | Работа с GitHub repositories, issues, PR, CI и публикацией локальных изменений. |
| `gmail` | `openai-curated-remote` | `0.1.2` | Поиск, чтение, triage, summary и draft/reply workflows для Gmail. |
| `pdf` | `openai-primary-runtime` | `26.614.11602` | Чтение, создание, рендеринг и визуальная проверка PDF. |
| `presentations` | `openai-primary-runtime` | `26.614.11602` | Создание, редактирование и проверка PowerPoint / slide deck артефактов. |
| `remotion` | `openai-curated` | `1.0.2` | Programmatic video creation на Remotion / React. |
| `spreadsheets` | `openai-primary-runtime` | `26.614.11602` | Работа с spreadsheet files: `.xlsx`, `.xls`, `.csv`, `.tsv`. |
| `vercel` | `openai-curated-remote` | `0.21.2` | Build/deploy web apps and agents, Vercel projects, deployments, env vars and logs. |

## Legacy / Duplicate Cache Copies

Эти папки есть локально, но выглядят как старые cached copies из `openai-curated`, потому что рядом уже есть `openai-curated-remote` копия того же plugin. Их не нужно документировать как отдельный актуальный plugin для onboarding-процесса.

| Plugin | Legacy cache path | Preferred cache path |
| --- | --- | --- |
| `clickup` | `openai-curated/clickup/43313cc9` | `openai-curated-remote/clickup/1.0.2` |
| `figma` | `openai-curated/figma/43313cc9` | `openai-curated-remote/figma/2.0.9` |
| `github` | `openai-curated/github/43313cc9` | `openai-curated-remote/github/0.1.2` |
| `vercel` | `openai-curated/vercel/43313cc9` | `openai-curated-remote/vercel/0.21.2` |

`remotion` сейчас найден только в `openai-curated/remotion/43313cc9`, поэтому он зафиксирован как актуальная локальная cache copy, а не как duplicate.

## Командные Skills, Которые Нужно Держать В Onboarding

Локальная пользовательская папка:

```text
C:\Users\PC\.codex\skills
```

На дату сверки в onboarding должны быть представлены все пользовательские skills из локальной папки:

| Skill | Статус в onboarding | Краткая ответственность |
| --- | --- | --- |
| `autofunnel-retrospective-analyzer` | добавлен | Post-run director для VK Auto Funnel API-only: планы, KPI, safety ledger, replies, social-life, candidate refill, cleanup и change log. |
| `det-ecosystem-doc-architect` | уже был | Архитектура документации после завершённых фич, релизов и артефактов DET ecosystem. |
| `knowledge-substrate-navigator` | уже был | Read-only сопоставление публичных Knowledge Substrate URLs с локальными strict UTF-8 Markdown sources. |
| `playwright` | добавлен | Terminal-first Playwright CLI automation для реального браузера, snapshots, screenshots, UI-flow debugging и data extraction. |
| `update-knowledge-docs` | уже был | Публикация review-ready Markdown версий из ClickUp workflow обратно в canonical Knowledge Substrate. |
| `windows-mojibake-first-aid` | уже был | First-response runbook для Windows mojibake в PowerShell, Git и Codex terminal. |

