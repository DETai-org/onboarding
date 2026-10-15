# Tools — вспомогательные инструменты DETai

В этой папке хранятся небольшие скрипты и другие вспомогательные материалы для настройки инструментов, которые команда использует в работе. Каждый файл сопровождается инструкцией в onboarding issues или кратким описанием здесь.

## Desktop Commander

- **[start-desktop-commander.ps1](start-desktop-commander.ps1)** — запуск Remote Desktop Commander на Windows с автоматическим выбором маршрута: через включённый локальный системный HTTP-прокси Windows (например, Happ) либо напрямую.
- [Пошаговый onboarding-туториал](https://github.com/DETai-org/onboarding/issues/35) — установка, авторизация, проверка и работа через Happ.
- [Настройка VPN Happ + Magnum](https://github.com/DETai-org/onboarding/issues/12).

Для использования скрипта необходимы Windows PowerShell, Node.js 24.5+ и глобально установленный пакет `@wonderwhy-er/desktop-commander`:

```cmd
npm install -g @wonderwhy-er/desktop-commander@latest
```

Скачай файл скрипта через GitHub (**Download raw file**) и сохрани, например, как `D:\dev\start-desktop-commander.ps1`. Запускай из CMD или PowerShell:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\dev\start-desktop-commander.ps1" -NetworkMode Auto
```

При `-NetworkMode Auto` скрипт использует **текущую глобально установленную версию**, не обновляет её и не меняет системные настройки. Включённый локальный системный прокси должен быть доступен; если он не работает, скрипт сообщает ошибку и не переключается незаметно на прямое соединение. Если системный прокси выключен, используется прямой режим. Для предварительной проверки без запуска агента добавь `-PlanOnly`.

Отключить запущенный агент можно сочетанием `Ctrl+C` в терминале. Не запускай вторую копию агента одновременно и не загружай скрипты из непроверенных источников.
