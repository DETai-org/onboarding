<%*
const targetPath = await tp.system.prompt("Куда создать (пример: 03_Проекты/01_VKontakte)")
const fullFolderPath = `${targetPath}/01_🧠Идеи_🎯Задачи`

try {
  await app.vault.createFolder(fullFolderPath)
} catch (e) {
  console.log("Папка уже существует")
}

// Получаем и увеличиваем ID
const idFile = await app.vault.read(tp.file.find_tfile("last_idea_id"))
const lastId = parseInt(idFile.trim())
const today = window.moment().format("YYYYMMDD")
let currentCounter = 1
const newBase = parseInt(today + "00")
const base = lastId >= newBase ? lastId : newBase

// ✅ Вставка ссылки на файл-таблицу
const linkToTable = `[[🎯Все задачи|Список всех задач🎯]]\n`

// ✅ Контент файлов с новой начинкой для первого и второго, остальные оставляем как есть
const files = {
  "01_🧠 Ещё мысль": `---\nideaID: ${base + currentCounter++}\n---\n\n> [!NOTE] – Ещё мысль\nЗдесь рождаются и накапливаются спонтанные мысли — наблюдения, догадки, образы и идеи, которые пока ещё не готовы стать частью формальной документации.  \n\nСм. [[Описание полотна мыслей]]`,
  
  "02_🎯 Задачи": `---\nideaID: ${base + currentCounter++}\n---\n\n${linkToTable} > [!TIP] — Сформируй список задач\n> <!--template-start-->\n> - [ ] Задача 1\n> <!--template-end-->`,

  // Сохраняем третий и четвёртый файлы без изменений
  "03_🔍 Узнать": `---\nideaID: ${base + currentCounter++}\n---\n\n${linkToTable} > [!TIP] — Сформируй список задач\n> <!--template-start-->\n> - [ ] Задача 1\n> <!--template-end-->`,
  
  "04_🛠 Исправить": `---\nideaID: ${base + currentCounter++}\n---\n\n${linkToTable} > [!TIP] — Сформируй список задач\n> <!--template-start-->\n> - [ ] Задача 1\n> <!--template-end-->`
}

// ✅ Создаём файлы
for (const [fileName, content] of Object.entries(files)) {
  await app.vault.create(`${fullFolderPath}/${fileName}.md`, content)
}

// ✅ Обновляем last_idea_id
const lastUsed = base + currentCounter - 1
await app.vault.modify(tp.file.find_tfile("last_idea_id"), `${lastUsed}`)
-%>