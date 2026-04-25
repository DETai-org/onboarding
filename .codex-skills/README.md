# 🧠 Командные Codex Skills DET

В экосистеме DET мы используем общие командные skills для Codex: они хранятся в репозитории, а каждый участник устанавливает их локально на свой компьютер.

Идея простая: команда договорилась о правилах, маршрутах и рабочих привычках один раз, а Codex на каждой машине получает одинаковый контекст и может помогать в одном стиле. Это снижает случайность, ускоряет онбординг и помогает не держать важные договорённости только в голове.

## 📦 Что лежит в этой папке

```text
.codex-skills/
  manifest.json
  README.md
  skills/
    det-ecosystem-doc-architect/
```

- `manifest.json` — индекс skills, их версий, путей и дат обновления.
- `skills/` — сами командные skills, которые можно установить локально.
- `README.md` — инструкция для участников команды.

## 🚀 Если вы новый участник

Откройте приложение Codex и вставьте в чат этот промпт:

```text
Используй skill-installer и установи Codex skill det-ecosystem-doc-architect из GitHub:
repo: DETai-org/onboarding
path: .codex-skills/skills/det-ecosystem-doc-architect

После установки проверь, что локально появился skill det-ecosystem-doc-architect, и скажи мне его версию.
```

После установки перезапустите Codex, чтобы новый skill появился в списке доступных навыков.

## 🔄 Как обновляться

Если нужно проверить, есть ли новая версия skill, можно попросить Codex:

```text
Сравни локальную версию skill det-ecosystem-doc-architect с версией в GitHub repo DETai-org/onboarding по manifest:
.codex-skills/manifest.json

Если в GitHub версия новее, покажи разницу версий и предложи обновление.
```

## 🛠 Текущий skill

### `det-ecosystem-doc-architect`

Версия: `0.1.0`

Назначение: помогает Codex выбирать, создавать и размещать документационные артефакты экосистемы DET по каноническим маршрутам: guide, explanation, standard, policy, reference, tutorial, how-to, log-summary и note.
