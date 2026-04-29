# Командные Codex Skills DET

Эта папка хранит общие Codex skills для команды DET / DETai.

Копия в репозитории является версионированным источником командных skills. Каждый участник может установить или обновить эти skills в локальную папку Codex, чтобы Codex на разных машинах работал с одинаковыми ролевыми моделями, рабочими процессами и каноническими маршрутами к базе знаний.

## Структура Папки

```text
.codex-skills/
  manifest.json
  README.md
  skills/
    det-ecosystem-doc-architect/
    knowledge-substrate-navigator/
```

- `manifest.json` — индекс shared skills: версии, пути, даты обновления и краткие описания.
- `skills/` — папки skills, которые можно копировать в `$CODEX_HOME/skills`.
- `README.md` — описание назначения и текущего состава командного реестра skills.

## Текущие Skills

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

## Заметки По Поддержке

- Держите `description` у skills узкими. Это поле влияет на неявный запуск skill, поэтому слишком широкие формулировки приводят к срабатыванию не в том контексте.
- Предпочитайте ролевые skills одному большому универсальному skill.
- Используйте `knowledge-substrate-navigator` как общую инфраструктурную способность для чтения канонических страниц Knowledge Substrate по браузерным ссылкам.
- При изменении shared skills синхронизируйте копию в репозитории и локальную копию в `$CODEX_HOME/skills`.
