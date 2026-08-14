# Командные Codex Skills DET

Эта папка хранит общие Codex skills для команды DET / DETai.

Копия в репозитории является версионированным источником командных skills. Каждый участник может установить или обновить эти skills в локальную папку Codex, чтобы Codex на разных машинах работал с одинаковыми ролевыми моделями, рабочими процессами и каноническими маршрутами к базе знаний.

## Структура Папки

```text
.codex-skills/
  manifest.json
  README.md
  skills/
    autofunnel-retrospective-analyzer/
    det-ecosystem-doc-architect/
    knowledge-substrate-navigator/
    log-summary/
    playwright/
    update-knowledge-docs/
    windows-mojibake-first-aid/
```

- `manifest.json` — индекс shared skills: версии, пути, даты обновления и краткие описания.
- `skills/` — папки skills, которые можно копировать в `$CODEX_HOME/skills`.
- `README.md` — описание назначения и текущего состава командного реестра skills.
- `codex-local-plugin-inventory.md` — снимок локальных Codex plugins в технической папке `.codex/plugins/cache`.

## Текущие Skills

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

Версия: `0.2.0`

Назначение: post-implementation / post-release архитектура документации для артефактов экосистемы DET.

Используйте этот skill после того, как проект, фича, релиз или версия дошли до осмысленного завершённого состояния и требуют документационной архитектуры: какие артефакты нужны, какую функцию документа они выполняют и где должны храниться.

Этот skill не должен использоваться для создания onboarding tutorial issues, выбора идеи, планирования Epic Issue, создания Work Package, написания кода или выполнения release/versioning-процесса, если пользователь явно не просит именно документационную архитектуру.

### `log-summary`

Версия: `0.1.0`

Назначение: компактный дневной журнал завершённой работы в ClickUp List `logs`
конкретного проекта, инструмента или инфраструктурного контура.

Skill использует локальный маршрут проекта, создаёт одну task
`Logs DD.MM.YYYY` на московскую рабочую дату, записывает форматированный
Markdown, добавляет подтверждённую provenance участника и при реальном
cross-project результате связывает отдельные локальные логи без копирования
одного отчёта во все контейнеры.

Объяснение skills, назначение `log-summary`, установка и локальный профиль
описаны в tutorial [«Codex skills и log-summary»](https://github.com/DETai-org/onboarding/issues/33).
Настройка нового локального проекта и его `AGENTS.md` продолжается в tutorial
[«Подключить log-summary к рабочему проекту»](https://github.com/DETai-org/onboarding/issues/32).

Путь к skill:

```text
.codex-skills/skills/log-summary
```

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

Назначение: публикация новых версий документов из ClickUp workflow
`Новые версии документов` обратно в канонический репозиторий
`Knowledge_substrate` с читаемым Git diff.

Используйте этот skill, когда:

- задача документа находится в статусе `READY FOR PUBLICATION`;
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

## ClickUp Prompts

Операционные prompts для установки и обновления командных Codex skills хранятся в ClickUp:

https://app.clickup.com/90152202658/v/li/901523014418

Текущие prompt-задачи:

- Установка командных Codex skills: https://app.clickup.com/t/86c9gt4zp
- Установка командных Codex skills с объяснением: https://app.clickup.com/t/86c9gt85g
- Обновление командных Codex skills: https://app.clickup.com/t/86c9gt50x
- Создание локального профиля участника DETai для Codex: https://app.clickup.com/t/86cb5ccf7

Командные карточки skills и их связи с исходниками:

https://app.clickup.com/90152202658/v/li/901525124627

История проектирования и сопровождения onboarding:

https://app.clickup.com/90152202658/v/li/901525128363

Каноническая модель onboarding:

https://detai-org.github.io/Knowledge_substrate/ru/onboarding/

Отдельный журнал прохождения onboarding новыми участниками:

https://app.clickup.com/90152202658/v/li/901525126396

## Заметки По Поддержке

- Держите `description` у skills узкими. Это поле влияет на неявный запуск skill, поэтому слишком широкие формулировки приводят к срабатыванию не в том контексте.
- Предпочитайте ролевые skills одному большому универсальному skill.
- Используйте `knowledge-substrate-navigator` как общую инфраструктурную способность для чтения канонических страниц Knowledge Substrate по браузерным ссылкам.
- При изменении shared skills синхронизируйте копию в репозитории и локальную копию в `$CODEX_HOME/skills`.
- Если локальная машина использует новые Codex plugins или cached plugin copies выглядят устаревшими, обновляйте `codex-local-plugin-inventory.md` вместе с этим README.
