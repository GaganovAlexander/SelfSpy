# SelfSpy
**SelfSpy** — это утилита для macOS, которая отслеживает активность системы и приложений.

## Текущие фичи
#### Оповещает о:
- Запуске и завершении работы системы
- Запуске и завершении работы всех оконных приложений
- Открытии и закрытии вкладок в Google Chrome и Safari
#### Приложение самостоятельно регистрируется как LaunchDaemon
#### Приложение запускается от root, чтобы видеть активность всех пользователей

## Установка
Перед установкой:
- Создайте Telegram-бота через [BotFather](https://t.me/BotFather), так как вам понадобится его токен.
- Узнайте свой Telegram ID с помощью [GetMyId](https://t.me/getmyid_bot) — он понадобится в setup.sh.

Далее просто запустите команды:

(Будет запрошен sudo пароль, так как, как сказано выше, приложение работает как LaunchDaemon от root пользователя)

(Могут быть запрошены разрешения для python на управление System Events и браузерами Google Chrome и Safari, так как оно напрямую опрашивает их, чтобы получить данные. Для работы приложения - нужно разрешение)
```sh
git clone https://github.com/GaganovAlexander/SelfSpy
cd SelfSpy
chmod 770 setup.sh
sudo ./setup.sh
```

## Управление приложением
Чтобы остановить приложение, используйте команду:
```sh
sudo launchctl unload /Library/LaunchDaemons/com.althgamer.selfspy.plist
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
- [LICENSE](https://github.com/GaganovAlexander/SelfSpy/blob/main/LICENSE) - лицензия MIT
- [setup.sh](https://github.com/GaganovAlexander/SelfSpy/blob/main/setup.sh) - скрипт установки, который создаёт окружение, регистрирует приложение в launchctl и настраивает права доступа  