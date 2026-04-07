"""
📌 Скрипт для переноса незавершённых задач из последнего дневного плана

- Ищет ВСЕ файлы планов формата `plan_YYYY-MM-DD.md`, включая подпапки.
- Извлекает дату из имени файла.
- Находит самый последний план до сегодняшнего дня.
- Переносит из него все незавершённые задачи (`- [ ]`) в текущий дневной план:
    - Вставляет в раздел `## 🕗 Предыдущие незавершённые задачи` по маркеру `<!-- ВСТАВИТЬ_ЗАДАЧИ -->`.
    - Удаляет перенесённые задачи из старого файла.
- Выводит лог: из какого файла взяты задачи и сколько их.
- Устойчив к разным названиям папок (в т.ч. с эмодзи) и структуре по месяцам.

⚠️ Обязательно запускать через `Templater` внутри Obsidian, чтобы путь к Vault был предопределён.
"""


import re
from pathlib import Path
import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

# === НАСТРОЙКИ ===
vault_path = Path("D:/Obsidian/Tasks_Center")
plan_folder = vault_path / "01_Планирование и Задачи" / "Планирование🎯" / "📅 План на день"
plan_files = list(plan_folder.glob("**/plan_*.md"))


# === ДАТЫ ===
today = datetime.date.today()



def find_latest_existing_plan(before_date):
    files = []
    for file in plan_folder.glob("**/plan_*.md"):

        match = re.match(r"plan_(\d{4})-(\d{2})-(\d{2})\.md", file.name)

        if match:
            y, m, d = match.groups()
            file_date = datetime.date(int(y), int(m), int(d))
            if file_date < before_date:
                files.append((file_date, file))
    return max(files, default=(None, None))[1]

prev_file = find_latest_existing_plan(today)

def format_date(date):
    # Убираем ведущий 0 вручную
    day = str(date.day)
    month = date.strftime("%B").replace("January", "января").replace("February", "февраля") \
        .replace("March", "марта").replace("April", "апреля").replace("May", "мая") \
        .replace("June", "июня").replace("July", "июля").replace("August", "августа") \
        .replace("September", "сентября").replace("October", "октября").replace("November", "ноября") \
        .replace("December", "декабря")
    year = str(date.year)
    return f"{day} {month} {year}"

def get_weekday_name(date):
    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    return days[date.weekday()]


# === ЛОГ ПЕРЕД ПЕРЕНОСОМ ===
if prev_file:
    print(f"📂 Задачи перенесены из файла: {prev_file.name}")
else:
    print("⚠️ Предыдущий файл с задачами не найден.")


# === ФАЙЛЫ ===
curr_file = next(plan_folder.glob(f"**/plan_{today.isoformat()}.md"), None)
if curr_file is None or not curr_file.exists():
    print("❌ Текущий файл с задачами не найден.")
    exit()


placeholder = "<!-- ВСТАВИТЬ_ЗАДАЧИ -->"



# === ПРОВЕРКА ФАЙЛОВ ===
if prev_file is None:
    print("❌ Предыдущий файл с задачами не найден.")
    exit()


# === ЧТЕНИЕ ТЕКСТОВ ===
prev_text = prev_file.read_text(encoding="utf-8")
curr_text = curr_file.read_text(encoding="utf-8")

# === ВЫБОР НЕЗАВЕРШЁННЫХ ЗАДАЧ ===
unfinished = re.findall(r"- \[ \] .+", prev_text)
unfinished_block = "\n".join(unfinished) + "\n"

# === ВСТАВКА В ШАБЛОН ===
if placeholder in curr_text:
    curr_text = curr_text.replace(placeholder, unfinished_block + "\n")
    print(f"✅ Вставлено {len(unfinished)} задач в место: '{placeholder}'")
else:
    print("⚠️ Маркер вставки не найден. Добавлено в конец.")
    curr_text += "\n" + unfinished_block

# === УДАЛЕНИЕ ИЗ ПРЕДЫДУЩЕГО ФАЙЛА ===
for task in unfinished:
    prev_text = prev_text.replace(task + "\n", "")

# === СОХРАНЕНИЕ ===
prev_file.write_text(prev_text, encoding="utf-8")
curr_file.write_text(curr_text, encoding="utf-8")

print("✅ Перенос завершён.")
