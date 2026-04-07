<%*
const months = {
  0: "января", 1: "февраля", 2: "марта", 3: "апреля", 4: "мая", 5: "июня",
  6: "июля", 7: "августа", 8: "сентября", 9: "октября", 10: "ноября", 11: "декабря"
}
const now = new Date()
const day = now.getDate()
const month = months[now.getMonth()]
const monthIndex = now.getMonth()
const year = now.getFullYear()
const weekday = tp.date.now("dddd")
const fileDate = `${year}-${(monthIndex + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`
const DateText = `${day} ${month} ${year}`


await tp.file.rename(`plan_${fileDate}`)

tR = `📅 ${DateText} (${weekday})\n\n`
tR += `🏷️ #\n\n`
tR += `## 🕗 *Предыдущие незавершённые задачи*\n\n`
tR += `<!-- ВСТАВИТЬ_ЗАДАЧИ -->\n\n`
tR += `## 🎯 Задачи\n\n\n\n`
tR += `## 🤖 Комментарий GPT\nGPT: Описание процесса, наблюдения, ошибки, результат.\n\n\n`
tR += `## ☁️ Моя мысль\n\n\n`
tR += `Логи и ссылки на документы 🧷⬇️\n\n\n`

 %>
