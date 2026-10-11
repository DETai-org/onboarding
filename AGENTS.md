# AGENTS.md

## Роль Workspace

`onboarding` — публичный командный маршрут входа в DET / DETai. Здесь живут
tutorial issues, общие Codex skills и материалы, которые участник получает для
первичной настройки рабочей среды.

Канонический командный реестр skills:

```text
D:\dev\DETai-org\onboarding\.codex-skills
https://github.com/DETai-org/onboarding/tree/main/.codex-skills
```

## Log Summary

Используй skill `log-summary`. Не создавай локальный `*log-summary.md`.

Основной маршрут этого репозитория — проект сопровождения onboarding
в Management Layer Team OS: [WorkLog List](https://team.detai-x.com/task-center/lists/de775f74-1778-54e0-ae09-b49807a1e6f6).
Разреши точный URL/UUID через Core, затем project и primary Logs через live
registry; проверь `kind: "list"`, `contentKind: "work_log"`, текущую version/ACL.
Используй дневной WorkLog и отдельный короткий personal checkpoint, не Task.

Каноническая модель onboarding описана в Knowledge Substrate:
https://detai-org.github.io/Knowledge_substrate/ru/onboarding/.

Не подменяй этот маршрут [WorkLog List прохождения участниками](https://team.detai-x.com/task-center/lists/526b6285-289e-5eb5-8c26-26ee57300edd):
он фиксирует tutorial progress и сохраняет отдельную classification
`Onboarding / participant-onboarding`. При материальной связи создай две
короткие записи и свяжи их, не смешивая management-работу с участническим прогрессом.

Если изменился соседний проект, разреши только его Core project/Logs и свяжи
короткие локальные итоги; не копируй весь отчёт. Начальный контекст не загружай
перед каждым CRUD. При отказе OAuth нужен reconnect/rescan Team-OS App; при
отсутствии маршрута — draft и причина. ClickUp API, navigation YAML и server
bearer не являются fallback.

## Team OS

- prompts для Codex: https://team.detai-x.com/task-center/lists/5c5ee31f-a307-50e9-8cc1-b333663869a0
- карточки командных skills: https://team.detai-x.com/task-center/lists/4de5bc43-0250-57d3-aa83-93ab38b449b7
- сопровождение onboarding: https://team.detai-x.com/task-center/lists/de775f74-1778-54e0-ae09-b49807a1e6f6
- прохождение onboarding участниками: https://team.detai-x.com/task-center/lists/526b6285-289e-5eb5-8c26-26ee57300edd

Для текста читай raw Markdown и version из канонического Core DTO выбранного
типа; не используй ClickUp description transport. Новая запись без уточнённого
типа — Task, explicit Note/WorkLog и редактирование выбранной записи сохраняют
её тип. Перед create проверь совместимость List, перед patch — expectedVersion.
