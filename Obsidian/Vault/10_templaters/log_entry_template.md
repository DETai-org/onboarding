<%*
const months = {
  0: "января", 1: "февраля", 2: "марта", 3: "апреля", 4: "мая", 5: "июня",
  6: "июля", 7: "августа", 8: "сентября", 9: "октября", 10: "ноября", 11: "декабря"
}
const weekdays = {
  0: "воскресенье", 1: "понедельник", 2: "вторник", 3: "среда", 4: "четверг", 5: "пятница", 6: "суббота"
}
const now = new Date()
const day = now.getDate()
const monthIndex = now.getMonth()
const month = months[monthIndex]
const year = now.getFullYear()
const weekday = weekdays[now.getDay()]
const fileDate = `${year}-${(monthIndex + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`
const Dateme = `${day} ${month} ${year}`



await tp.file.rename(`log_${fileDate}`)

tR = `📅 ${Dateme} (${weekday})\n\n`

tR += `🏷️ #добавь_хэштэг\n\n`
tR += `🤖 Чат с GPT по задачам дня (ссылка)  \n`

tR += `## Логи за день\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n`
tR += `> [!SUCCESS] 🎯 КВЦ достигнута  \n`
tR += `_Какая одна критически важная цель была достигнута сегодня?_  \n\n`
tR += `___\n🧷Ссылка на задачи дня:\n[[plan_${fileDate}|План на ${Dateme}]]\n`


%>

