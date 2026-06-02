---
repo: 'DETai-org/onboarding'
issue_number: 30
title: 'Windows UTF-8 baseline для Codex: устраняем кракозябры в PowerShell и Git'
state: 'OPEN'
url: 'https://github.com/DETai-org/onboarding/issues/30'
author_login: 'Anton-Psy'
author_name: 'Anton 🌓'
created_at: '2026-05-06T22:22:04Z'
updated_at: '2026-05-07T10:09:59Z'
closed_at: null
comments_count: 0
labels: []
milestone:
  number: 3
  title: '3 шаг'
  description: null
  due_on: null
assignees: []
snapshot:
  season: 'Spring 2026'
  date: '2026-06-02'
---

# Issue #30: Windows UTF-8 baseline для Codex: устраняем кракозябры в PowerShell и Git

## Контекст 🎯

При локальной работе на Windows (PowerShell + Git + Codex) периодически возникают «кракозябры» и нечитаемая кириллица (`Ð...`, `Р...`).

Это ломает диагностику, делает логи и сообщения трудночитаемыми и усложняет работу в нескольких репозиториях сразу.

Этот туториал фиксирует единый baseline для машины:

- актуальный PowerShell 7;
- UTF-8 настройки терминала;
- Git global encoding;
- подключение и использование командного skill `windows-utf8-guard`.


_Примечание по терминам:_

машина=ваш компютер за которым вы работаете 😊

---

## Что мы делаем в этом шаге

1. Проверяем текущую версию PowerShell и кодировку сессии.
2. Устанавливаем/обновляем PowerShell через `winget`.
3. Включаем UTF-8 настройки для терминала.
4. Нормализуем Git global encoding.
5. Подключаем skill, который помогает быстро диагностировать и чинить подобные проблемы в будущем.

---

## Шаг 1. Проверка текущего состояния

Откройте PowerShell и выполните:

```powershell
pwsh -v
[Console]::OutputEncoding
chcp
```

Ожидаемый baseline:

- PowerShell 7.x
- `OutputEncoding` = UTF-8
- `Active code page: 65001`

---

## Шаг 2. Обновление PowerShell через winget

```powershell
winget install --id Microsoft.PowerShell --source winget
```

После установки перезапустите терминал и повторно проверьте версию:

```powershell
pwsh -v
```

---

Вот готовый вариант **Шага 3** с расширением, полностью в Markdown-разметке, готовый к публикации:


## Шаг 3. UTF-8 для текущей сессии и постоянная настройка профиля

Если текст в терминале уже «поехал», примените сразу в текущем окне:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
````

### Настройка постоянной кодировки для PowerShell

Чтобы UTF-8 включался автоматически при каждом запуске терминала:

1. Откройте профиль PowerShell в редакторе (блокноте):

В окне PowerShell введите
```powershell
notepad $PROFILE
```
После этого откроется файл.

2. Вставьте в файл:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

> ⚠️ Примечание:
>
> * Для PowerShell 7 (`pwsh`) используется отдельный профиль от PowerShell 5.1.
> * Установка PowerShell 7 **не ломает** текущие настройки 5.1, и наоборот.
> * Это гарантирует стабильный UTF-8 при каждом запуске терминала.

### Быстрая проверка кириллицы

Чтобы убедиться, что UTF-8 работает корректно, выполните:

```powershell
Write-Output "Привет, мир! 🚀"
```

* Если вывод читаемый и эмодзи отображаются, значит кодировка настроена правильно.

---

## Шаг 4. Git global encoding

Выполните один раз на машине:

```powershell
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8
git config --global core.quotepath false
git config --global gui.encoding utf-8
```

Проверка:

```powershell
git config --global --get i18n.commitEncoding
git config --global --get i18n.logOutputEncoding
git config --global --get core.quotepath
git config --global --get gui.encoding
```

---

## Шаг 5. Подключение skill для повторного использования

В репозитории `onboarding` добавлен skill:

- Путь: `.codex-skills/skills/windows-utf8-guard`
- Файл: `.codex-skills/skills/windows-utf8-guard/SKILL.md`

Прямая ссылка:

- https://github.com/DETai-org/onboarding/tree/main/.codex-skills/skills/windows-utf8-guard

Этот skill нужен, когда:

- снова появляется нечитаемая кириллица в терминале;
- нужно быстро пройти диагностический чеклист;
- нужно стабилизировать кодировку без долгого ручного дебага.

---

## Почему это важно

- Экономит время на каждом проекте, а не только в одном репозитории.
- Снижает риск ложной диагностики (когда кажется, что «сломался файл», а сломана только кодировка вывода).
- Формирует единый стандарт рабочего окружения для команды.

---

## Результат ✅

После выполнения шага:

- PowerShell и Git работают в стабильном UTF-8 baseline.
- Кириллица в логах и выводах читается корректно.
- В команде есть переиспользуемый skill для быстрой диагностики и устранения проблем кодировки.

## Comments

_No comments._
