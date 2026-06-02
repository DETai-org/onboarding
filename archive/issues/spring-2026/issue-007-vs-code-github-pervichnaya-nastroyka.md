---
repo: 'DETai-org/onboarding'
issue_number: 7
title: 'VS Code + GitHub — первичная настройка'
state: 'OPEN'
url: 'https://github.com/DETai-org/onboarding/issues/7'
author_login: 'Anton-Psy'
author_name: 'Anton 🌓'
created_at: '2026-02-10T14:00:13Z'
updated_at: '2026-05-05T15:03:46Z'
closed_at: null
comments_count: 1
labels:
  - name: 'setup'
    color: '0e8a16'
    description: 'Подготовка и настройка рабочего окружения, инструментов или доступов перед началом работы.'
  - name: '🎓 Tutorial'
    color: '5CDEF5'
    description: 'Обучающий документ для первого прохода. Формирует понимание системы.'
  - name: '🧰 Tools'
    color: 'c5def5'
    description: null
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

# Issue #7: VS Code + GitHub — первичная настройка

# VS Code + GitHub — первичная настройка (Local workflow)

Перед прохождением данного туториала читай в базе знаний [Роль VS Code в экосистеме](https://detai-org.github.io/Knowledge_substrate/ru/ecosystem/Tools/VS_Code/)


> [!NOTE]
> Этот туториал описывает базовый сценарий, когда работа ведётся локально в VS Code,
> а изменения попадают в GitHub через Commit + Push.
> Ветка с подключением к серверу по SSH — отдельный туториал.

## Цель 🎯
После выполнения ты сможешь:
- клонировать репозиторий из GitHub-организации DETai-org на компьютер;
- редактировать Markdown с live preview;
- отправлять изменения в GitHub (Commit → Push);
- получать обновления с GitHub (Fetch / Pull).
- скачать ClickUp приложение на комп 🤩

## Что нужно заранее
- GitHub-аккаунт и доступ к репозиториям DETai-org.
- Windows 10/11

## Шаг 1. Установить VS Code

1. Скачать **Visual Studio Code (User Installer)**:
   - Официальная страница: https://code.visualstudio.com/
2. Установить как обычно.
3. На шаге “Дополнительные задачи” в установщике включить:
   - ✅ **Add to PATH** (доступно после перезагрузки)
   - ✅ (опционально) “Open with Code” в контекстном меню проводника

## Шаг 2. (Рекомендуется) Создать структуру папок на диске
Рекомендуемая структура:
- `D:/dev/DETai-org/`
Дальше каждый репозиторий клонируется внутрь этой папки

---

## Шаг 3. Установить Git (обязательный шаг)

> Git нужен VS Code для клонирования репозиториев, отслеживания изменений и отправки правок в GitHub (Commit / Push).
> Без Git кнопка **Clone Repository** и команды `Git:` работать не будут.

### 3.1 Скачать Git

1. Открой официальный сайт Git:
   👉 [https://git-scm.com/download/win](https://git-scm.com/download/win)

2. Нажми **Click here to download** — начнётся загрузка установщика **Git for Windows**.

---

### 3.2 Установка Git (что выбирать)

Запусти скачанный установщик и **на всех шагах жми `Next`**, **кроме следующих пунктов**:

#### 🔹 Компоненты

Оставь настройки **по умолчанию** (ничего не меняй).

#### 🔹 Default editor for Git

Выбери: **Use Visual Studio Code as Git’s default editor**

> Это важно — Git будет открывать сообщения коммитов именно в VS Code.

#### 🔹 Initial branch name

Выбери: **Let Git decide**

(Для работы с существующими репозиториями это не влияет.)

#### 🔹 PATH environment

Выбери: **Git from the command line and also from 3rd-party software (Recommended)**

> Это позволяет VS Code и системе находить Git автоматически.

#### 🔹 SSH executable

Выбери: **Use bundled OpenSSH**

#### 🔹 HTTPS transport backend

Выбери: **Use the native Windows Secure Channel library**

#### 🔹 Line endings

Оставь: **Checkout Windows-style, commit Unix-style line endings (Recommended)**

#### 🔹 Terminal emulator

Оставь: **Use MinTTY (default terminal of MSYS2)**

#### 🔹 `git pull` behavior

Оставь: **Fast-forward or merge**

После этого: * нажми **Install** дождись завершения и закрой установщик

---

### 3.3 Перезапустить VS Code

⚠️ **Важно:**
Если VS Code был открыт — **полностью закрой и открой его заново**.

После этого:

* в стартовом окне появится кнопка **Clone Repository**
* команды `Git:` станут доступны через Command Palette

---

### ✅ Результат шага

После выполнения этого шага:

* Git установлен в системе
* VS Code видит Git
* можно клонировать репозитории из GitHub

---

## Шаг 4. Клонировать репозиторий из GitHub в VS Code

На этом шаге мы **скачиваем репозиторий с GitHub на компьютер**, чтобы работать с файлами на компе в VS Code.

Клонирование — это создание **локальной копии репозитория**, связанной с GitHub.  
Все изменения ты будешь делать у себя на компьютере и затем отправлять обратно на GitHub.

В рамках онбординга обязательно клонируем репозиторий:

```text
https://github.com/DETai-org/onboarding.git
```

Итоговый локальный путь должен получиться таким:

```text
D:/dev/DETai-org/onboarding
```

Этот репозиторий потом понадобится в tutorial по Codex: его нужно будет добавить как проект в приложении Codex и из него установить командные skills.

### Как это сделать (HTTP-способ)

1. Открой VS Code  
   Ты увидишь стартовый экран без открытой папки.

2. Нажми **Clone Git Repository…**  
   (если стартовый экран закрыт — открой командную палитру `Ctrl + Shift + P` и введи `Git: Clone`)

3. Вставь HTTPS-ссылку на репозиторий onboarding:

   ```text
   https://github.com/DETai-org/onboarding.git
   ```

4. Выбери **папку на компьютере**, куда будет сохранён репозиторий:  
   `D:/dev/DETai-org/`

5. После клонирования VS Code предложит открыть репозиторий — нажми **Open**.

6. Проверь, что открытая папка называется `onboarding`.


## Шаг 5. Workspace Trust
При первом открытии VS Code спросит доверие к файлам.
- Выбери **Trust the authors** ➕ (опционально) доверять всему `DETai-org`, чтобы не спрашивал для каждого репо.

______

## Шаг 6. Отправить изменения в GitHub (Commit → Push)

Измени какой-нибудь файл

1) Открой Source Control: `Ctrl+Shift+G`
2) Убедись, что файлы видны в списке изменений
3) Напиши commit message
4) Нажми **Commit**
   - если VS Code спросит про unsaved files: **Save All & Commit Changes**

Тут Git должен знать, **кто именно делает изменения**.  
Для этого нужно один раз указать **имя пользователя** и **email**, привязанные к твоему GitHub-аккаунту.

Без этого Git **не позволит сделать Commit**.

В VS Code: Открой **Terminal** (`Terminal → New Terminal` или ``Ctrl + ` ``) и  выполни команды (подставь свои данные):

```bash
git config --global user.name "Anton Kolhonen"
git config --global user.email "email@который_у_тебя_в_GitHub"
```

⚠️ Email **должен совпадать** с тем, что указан в GitHub
(или быть добавлен в GitHub как дополнительный).

Проверь:

```bash
git config --global --list
```

5) Нажми **Push** или **Sync Changes**

6) Проверь изменения в GitHub Web если изменения видны в веб-версии - это успех 🎉🎉🎉


# Результат 🎯✅

В результате ты получаешь:

— локально настроенный VS Code, готовый к работе с GitHub;  
— установленный и корректно подключённый Git;  
— локальную копию репозитория `DETai-org/onboarding` на компьютере;  
— рабочий цикл **изменения → commit → push** без терминала;  
— возможность забирать обновления из GitHub (fetch / pull);  
— комфортную среду для работы с Markdown и документацией.

Ты теперь работаешь в режиме:

🖥️ **Локальный VS Code**  
🔗 **Связь с GitHub**  
📁 **Репозиторий на диске**  
📝 **Редактирование + live preview**  
🚀 **Commit → Push без боли**

Это базовый, надёжный фундамент. 

______

## Частые вопросы
### “Почему не видно файлов в CHANGES?”
- Возможны `STAGED CHANGES` или несохранённые файлы.
- Commit требует commit message.

### “Можно ли одновременно править и в Web, и локально?”
Можно, но соблюдай правило:
- перед локальной работой — Pull/Sync
- после локальной — Commit → Push
____

# Дополнительные настройки для удобства ➕

#### Цветовые настройки темы 👁️‍🗨️

Нажми

```
Ctrl + K → Ctrl + T
```
Выбери:

☀️ **Quiet Light** — Это  по сути, это тема «для чтения и мышления» 
тексты / Markdown / документация

🕶️ **Monokai** Классический хакерский вайб (из коробки VS Code) 👉 **икона хакерства №1**

🌌 **Abyss**  Атмосферный вайб (если захочешь эстетики)\
Подходит для: долгих ночных сессий, когда хочется «исчезнуть в коде».

#### Просмотр файлов

Markdown Preview (живой просмотр)
- Preview: `Ctrl+Shift+V`   или Preview to the Side: `Ctrl+K`, затем `V`

  - поиск файла по имени (`Ctrl + P`);
  - поиск по содержимому (`Ctrl + Shift + F`);

_Любые другие команды и вопросы для углубления в тематику Уточняй у gpt_

## 🚀 Хочешь понять, глубже?

Если ты прошёл этот туториал и хочешь разобраться глубже — зачем нужен Git, как он помогает командам и почему мы работаем именно так, можешь использовать ChatGPT как проводника.

Попробуй задать ему такой вопрос:

```markdown
Объясни простыми словами:

- зачем вообще придумали Git  
- что такое версионность и зачем она нужна  
- как Git помогает командам работать вместе и не ломать друг другу код  
- чем отличается локальная работа от работы через сервер  
- Кто придумал GitHub как это связанно с Git и при чем тут Билл Гейтс? 😅

Представь, что я только начал работать с Git и VS Code и хочу понять не кнопки, а общую логику и смысл этого подхода.
```




## Comments

### Comment 1

- Author: `VsePsy`
- Created: `2026-05-05T15:03:46Z`
- URL: https://github.com/DETai-org/onboarding/issues/7#issuecomment-4380521962
- Author association: `MEMBER`
- Includes created edit: `False`

В шаге 6, нужно уточнить где именно находятся файлы. Я не очень понял. У меня например во вкладке CHАNGES ничего нет. Но вижу какие-то кое-что во вкладке GRAPH.

> 2. Убедись, что файлы видны в списке изменений

