# SelfSpy
**SelfSpy** — это утилита для macOS, которая отслеживает активность системы и приложений.

## Текущие фичи
#### Оповещает о:
- Запуске и завершении работы системы
- Запуске и завершении работы всех оконных приложений
- Открытии и закрытии вкладок в Google Chrome и Safari
- Добавлении и удалении cron задач
- Установку и удаление приложений
- Загрузка dmg файлов
#### Приложение самостоятельно регистрируется как LaunchDaemon
#### Приложение запускается от root, чтобы видеть активность всех пользователей

## Установка
Перед установкой:
- Создайте Telegram-бота через [BotFather](https://t.me/BotFather), так как вам понадобится его токен.
- Узнайте свой Telegram ID с помощью [GetMyId](https://t.me/getmyid_bot) — он понадобится в setup.sh.

Далее просто запустите команды:

(Будет запрошен sudo пароль, так как, как сказано выше, приложение работает как LaunchDaemon от root пользователя)

(Могут быть запрошены разрешения для python на управление System Events и браузерами Google Chrome и Safari, так как оно напрямую опрашивает их, чтобы получить данные. А так же на просмотр папок Downloads у пользователей. Для работы приложения - нужно разрешение)
```sh
git clone https://github.com/GaganovAlexander/SelfSpy
cd SelfSpy
chmod 770 setup.sh
sudo ./setup.sh
```
После отработки скрипта помимо всех настроек и автозапуска, будут созданы скрипты start.sh и stop.sh для упрощёного запуска и остановки приложения по необходимости.

**ВАЖНО!** Скрипт сразу даёт приложению автозапуск со включением системы, так что запускать start.sh после перезагрузок НЕ надо!
## Управление приложением
Чтобы остановить приложение, используйте команду:
```sh
sudo ./start.sh
```
Чтобы заново(или, если по какой-то причине не запустилось само с запуском системы) запустить:
```sh
sudo launchctl load /Library/LaunchDaemons/com.althgamer.selfspy.plist
```
---
Для полного удаления приложения:
```sh
sudo launchctl unload /Library/LaunchDaemons/com.althgamer.selfspy.plist
sudo rm /Library/LaunchDaemons/com.althgamer.selfspy.plist
```
Тут заменить "{path_}" на путь до директории "SelfSpy/" включительно
```sh
sudo rm -rf {path_}
```
---

## Структура приложения
- [src/](https://github.com/GaganovAlexander/SelfSpy/blob/main/src) - исходный код приложения
- [src/saved_data/](https://github.com/GaganovAlexander/SelfSpy/blob/main/src/saved_data) - хранилище для данных, сохраняемых между запусками приложения или при отсутствии интернета
- [LICENSE](https://github.com/GaganovAlexander/SelfSpy/blob/main/LICENSE) - лицензия MIT
- [setup.sh](https://github.com/GaganovAlexander/SelfSpy/blob/main/setup.sh) - скрипт установки, который создаёт окружение, регистрирует приложение в launchctl и настраивает права доступа  
- [start.sh](https://github.com/GaganovAlexander/SelfSpy/blob/main/start.sh) - скрипт быстрого запуска приложения. Создаётся при запуске setup.sh (Запускать от sudo)
- [stop.sh](https://github.com/GaganovAlexander/SelfSpy/blob/main/stop.sh) - скрипт быстрой остановки приложения. Создаётся при запуске setup.sh (Запускать от sudo)