const { exec } = require("child_process");

module.exports = async function () {
  new Notice("🚀 Запускаю скрипт переноса задач...");

  exec('"C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe" "D:/Obsidian/Tasks_Center/11_core_scripts/move_pending_tasks.py"', (err, stdout, stderr) => {
    if (err) {
      console.error("❌ Ошибка скрипта:", stderr);
      new Notice("❌ Ошибка при запуске скрипта.\nПодробности в консоли разработчика (Ctrl+Shift+I)");
      return;
    }

    console.log("✅ Скрипт выполнен:\n", stdout);
    new Notice("✅ Задачи успешно перенесены!");
  });
};
