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
  list_id: "901525128363"
  list_url: "https://app.clickup.com/90152202658/v/li/901525128363"
  scope: Governance
  context: onboarding-management
  navigation_key: onboarding_management
  global_navigation: D:\dev\DETai-org\Management_Layer\docs\clickup-navigation\index.yaml
```

Основной маршрут этого репозитория — List `logs` в Folder `Onboarding` внутри
Space `Management Layer`. Здесь владельцы проектируют, обновляют и сопровождают
onboarding. Для обычной работы не сканируй весь ClickUp.

Каноническая модель onboarding, его GitHub- и ClickUp-контуры описаны в
Knowledge Substrate:
https://detai-org.github.io/Knowledge_substrate/ru/onboarding/.

Не подменяй этот маршрут List `logs` из отдельного Space `Onboarding`: тот
контейнер фиксирует прохождение tutorial-задач новыми участниками и использует
classification `Onboarding / participant-onboarding`. При материальной связи
создай две короткие записи и свяжи их, не смешивая management-работу с
участническим прогрессом.

Если завершённая работа материально изменила соседний проект или инструмент,
используй `global_navigation`, найди только его маршрут, live-проверь List
`logs` и создай отдельный короткий фрагмент в его дневной записи. Свяжи два
лога ссылками и не копируй один отчёт целиком.

## ClickUp

- prompts для Codex: https://app.clickup.com/90152202658/v/li/901523014418
- карточки командных skills: https://app.clickup.com/90152202658/v/li/901525124627
- сопровождение onboarding: https://app.clickup.com/90152202658/v/li/901525128363
- прохождение onboarding участниками: https://app.clickup.com/90152202658/v/li/901525126396

Текст task description, содержащий Markdown, передавай через
`markdown_description`; при чтении запрашивай
`include_markdown_description=true`.
