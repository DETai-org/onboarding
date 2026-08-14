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

```yaml
log_summary:
  list_id: "901525126396"
  scope: Governance
  context: onboarding
  navigation_key: onboarding
  global_navigation: D:\dev\DETai-org\Management_Layer\docs\clickup-navigation\index.yaml
```

Основной маршрут — List `logs` в ClickUp Folder `Туториалы правки` внутри
Space `Onboarding`. Для обычной onboarding-работы не сканируй весь ClickUp.

Если завершённая работа материально изменила соседний проект или инструмент,
используй `global_navigation`, найди только его маршрут, live-проверь List
`logs` и создай отдельный короткий фрагмент в его дневной записи. Свяжи два
лога ссылками и не копируй один отчёт целиком.

## ClickUp

- prompts для Codex: https://app.clickup.com/90152202658/v/li/901523014418
- карточки командных skills: https://app.clickup.com/90152202658/v/li/901525124627
- onboarding logs: https://app.clickup.com/90152202658/v/li/901525126396

Текст task description, содержащий Markdown, передавай через
`markdown_description`; при чтении запрашивай
`include_markdown_description=true`.
