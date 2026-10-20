# Командные Skills DET

Эта папка хранит общие Skills команды DET / DETai: отдельные навыки для
индивидуальной установки в Codex и наборы навыков MCP-плагинов ChatGPT.

Копия в репозитории является версионированным источником командных skills. Каждый участник может установить или обновить эти skills в локальную папку Codex, чтобы Codex на разных машинах работал с одинаковыми ролевыми моделями, рабочими процессами и каноническими маршрутами к базе знаний.

## Структура Папки

```text
.codex-skills/
  manifest.json
  README.md
  MCP Skills/
    Team-OS/
      README.md
      start-work/
      log-summary/
      update-orientations/
  skills/
    autofunnel-retrospective-analyzer/
    det-ecosystem-doc-architect/
    knowledge-substrate-navigator/
    playwright/
    update-knowledge-docs/
    windows-mojibake-first-aid/
```

- `manifest.json` — индекс shared skills и групп навыков плагинов: версии, пути, даты обновления и краткие описания.
- `skills/` — отдельные навыки для индивидуальной установки в `$CODEX_HOME/skills`.
- `MCP Skills/` — наборы навыков MCP-плагинов, сгруппированные по имени плагина.
- `README.md` — описание назначения и текущего состава командного реестра skills.

## Текущие Skills

### Набор плагина `Team-OS`

Версия набора: `1.3.1`.

Три Skills существующего плагина ChatGPT сгруппированы в
[`.codex-skills/MCP Skills/Team-OS`](<MCP Skills/Team-OS/README.md>): `start-work`,
`log-summary` и `update-orientations`. В README набора находятся установка
через GitHub и Plugin Creator и готовый промпт для личного аккаунта участника.
`Team-OS/` — группа, которую не устанавливают как один локальный Skill.
Запись набора находится отдельно в `plugin_skill_bundles` manifest;
остальные локальные skills по-прежнему перечислены в `skills`.

### `autofunnel-retrospective-analyzer`

Версия: `3.5.1`

Назначение: post-run директор и self-improving maintainer для `VK/auto_funnel` в API-only режиме.

Используйте этот skill после завершённого запуска VK Auto Funnel, когда нужно разобрать свежий runner/state/history, API-call ledger и safety incidents; обновить per-profile `api_direct_plan.json`; подготовить first messages, inbound replies и social-life actions; настроить KPI, pacing, friend sources и candidate refill; проверить cross-profile dedup; убрать dead paths; записать change log директора.

Это специфический skill. Используйте его только при наличии доступа к репозиторию WK и рабочему контуру `VK/auto_funnel`.

Путь к skill:

```text
.codex-skills/skills/autofunnel-retrospective-analyzer
```

### `knowledge-substrate-navigator`

Версия: `0.1.1`

Назначение: read-only навигация по документации DETai Knowledge Substrate.

Используйте этот skill, когда Codex получает публичную MkDocs-ссылку на Knowledge Substrate или должен найти и прочитать канонический документ из локального клона.

Основной локальный путь к Knowledge Substrate:

```text
D:\dev\DETai-org\Knowledge_substrate
```

Skill сопоставляет публичные URL с локальными Markdown-файлами внутри:

```text
knowledge_core/source_of_truth/docs
```

Он читает Markdown как strict UTF-8 и игнорирует кодовые части репозитория, generated-папки, кэши, логи и `.git`.

### `det-ecosystem-doc-architect`

Версия: `0.2.3`

Назначение: post-implementation / post-release архитектура документации для артефактов экосистемы DET.

Используйте этот skill после того, как проект, фича, релиз или версия дошли до осмысленного завершённого состояния и требуют документационной архитектуры: какие артефакты нужны, какую функцию документа они выполняют и где должны храниться.

Этот skill не должен использоваться для создания onboarding tutorial issues, выбора идеи, планирования Epic Issue, создания Work Package, написания кода или выполнения release/versioning-процесса, если пользователь явно не просит именно документационную архитектуру.

### `playwright`

Версия: `0.1.0`

Назначение: terminal-first автоматизация реального браузера через Playwright CLI.

Используйте этот skill, когда Codex должен открыть страницу, пройти UI-flow, заполнить форму, снять snapshot/screenshot, проверить локальный frontend или извлечь данные из браузерной страницы. Это техническая утилита для браузерной проверки и отладки, а не DET-специфичная ролевая модель.

Путь к skill:

```text
.codex-skills/skills/playwright
```

### `windows-mojibake-first-aid`

Версия: `0.2.1`

Назначение: короткий first-response runbook на случай кракозябр в Windows-окружении при работе с PowerShell, Git и Codex.

Используйте этот skill, когда:

- в терминале внезапно ломается кириллица (`Ð...`, `Р...`, нечитаемый текст);
- нужно быстро применить безопасный session-level UTF-8 reset и повторить проблемную команду;
- требуется понять, решается ли инцидент в текущей сессии или уже нужен возврат к machine-level baseline из onboarding.

Путь к skill:

```text
.codex-skills/skills/windows-mojibake-first-aid
```

### `update-knowledge-docs`

Версия: `0.1.0`

Назначение: публикация новых версий документов из редакционного Task/Note Team OS
`Новые версии документов` обратно в канонический репозиторий
`Knowledge_substrate` с читаемым Git diff.

Используйте этот skill, когда:

- Task находится в workflow `READY FOR PUBLICATION`, либо публикация Note явно согласована; Note не получает Task status;
- нужно перенести подготовленный Markdown обратно в канонический источник;
- важно сохранить reviewable diff вместо полного переформатирования файла;
- требуется пройти цикл `dry-run -> preview -> diff gate -> apply -> PR`.

Путь к skill:

```text
.codex-skills/skills/update-knowledge-docs
```

## Установка И Обновление

Установите или обновите skill, скопировав папку из:

```text
.codex-skills/skills/<skill-name>
```

в:

```text
C:\Users\PC\.codex\skills\<skill-name>
```

После установки или обновления перезапустите Codex, чтобы новые или изменённые skills появились в списке доступных навыков.

## Prompts и карточки Team OS

Операционные prompts для установки и обновления командных Codex skills хранятся как Notes в Team OS:

https://team.detai-x.com/task-center/lists/5c5ee31f-a307-50e9-8cc1-b333663869a0

Текущие prompt-заметки:

- Установка командных Codex skills: https://team.detai-x.com/notes/1396e87f-b8a9-5fe6-8d9f-d77bd723fec8
- Установка командных Codex skills с объяснением: https://team.detai-x.com/notes/1bdd70ae-8473-56a9-857f-4815413f3944
- Обновление командных Codex skills: https://team.detai-x.com/notes/e4c090f6-2547-55ed-8e71-2a99133da960
- Создание локального профиля участника DETai для Codex: https://team.detai-x.com/notes/6944cb26-9078-514d-a4dd-6b982a7288f0

Командные карточки skills и их связи с исходниками:

https://team.detai-x.com/task-center/lists/4de5bc43-0250-57d3-aa83-93ab38b449b7

История проектирования и сопровождения onboarding:

https://team.detai-x.com/task-center/lists/de775f74-1778-54e0-ae09-b49807a1e6f6

Каноническая модель onboarding:

https://detai-org.github.io/Knowledge_substrate/ru/onboarding/

Отдельный журнал прохождения onboarding новыми участниками:

https://team.detai-x.com/task-center/lists/526b6285-289e-5eb5-8c26-26ee57300edd

## Заметки По Поддержке

- Держите `description` у skills узкими. Это поле влияет на неявный запуск skill, поэтому слишком широкие формулировки приводят к срабатыванию не в том контексте.
- Предпочитайте ролевые skills одному большому универсальному skill.
- Используйте `knowledge-substrate-navigator` как общую инфраструктурную способность для чтения канонических страниц Knowledge Substrate по браузерным ссылкам.
- При изменении shared skills синхронизируйте копию в репозитории и локальную копию в `$CODEX_HOME/skills`.
