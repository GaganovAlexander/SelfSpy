import urllib.parse
import urllib.request
from datetime import datetime
import sys

from configs import TG_BOT_TOKEN, TG_CHAT_ID, state
from storage import load_backlog, save_backlog, save_cron, save_apps, save_dmgs


def send_to_telegram(message, is_from_flush_backlog=False):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    req = urllib.request.Request(url, data)
    try:
        with urllib.request.urlopen(req) as response:
            response.read()
        return True
    except:
        if not is_from_flush_backlog:
            backlog = load_backlog()
            backlog.append(message)
            save_backlog(backlog)
        return False

def handle_event(event_type, *args):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    match event_type:
        case "start":
            message = (
                "🚀 *Приложение запущено*\n"
                f"🕒 *Время:* `{timestamp}`\n"
                f"🔹 *Имя приложения:* `{args[0]}`"
            )
        case "stop":
            message = (
                "⛔ *Приложение закрыто*\n"
                f"🕒 *Время:* `{timestamp}`\n"
                f"🔹 *Имя приложения:* `{args[0]}`"
            )
        case "open_url":
            message = (
                "🆕 *Новый URL открыт*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"🌐 *Браузер*: `{args[0]}`\n"
                f"🔗 *URL*: [{urllib.parse.urlparse(args[1]).netloc}]({args[1]})"
                )
        case "close_url":
            message = (
                "❌ *URL закрыт*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"🌐 *Браузер*: `{args[0]}`\n"
                f"🔗 *URL*: [{urllib.parse.urlparse(args[1]).netloc}]({args[1]})"
                )
        case "new_cron":
            message = (
                "➕ *Новая cron-задача*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"👤 *Пользователь*: `{args[0]}`\n"
                f"📝 *Задача*:\n```\n{args[1]}\n```"
            )
        case "deleted_cron":
            message = (
                "➖ *Удалена cron-задача*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"👤 *Пользователь*: `{args[0]}`\n"
                f"📝 *Задача*:\n```\n{args[1]}\n```"
            )
        case "installed":
            message = (
                "📦 *Установлено приложение*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"🖥️ *Приложение*: `{args[0]}`"
            )
        case "uninstalled":
            message = (
                "🗑️ *Удалено приложение*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"🖥️ *Приложение*: `{args[0]}`"
            )
        case "downloaded_dmg":
            message = (
                "📥 *Загружен DMG-файл*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"📄 *Файл*: `{args[0]}`"
            )


    flush_backlog()
    send_to_telegram(message)


def flush_backlog():
    backlog = load_backlog()
    if not backlog:
        return
    for message in backlog:
        if not send_to_telegram(message, True):
            break
    else:
        save_backlog([])

def on_startup():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🖥 *Система запущена*\n🕒 *Время:* `{timestamp}`"
    flush_backlog()
    send_to_telegram(message)

def on_shutdown(signum, frame):
    save_cron(state["crontasks"])
    save_apps(list(state["apps"]))
    save_dmgs(list(state["dmgs"]))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔌 *Система выключается*\n🕒 *Время:* `{timestamp}`"
    flush_backlog()
    send_to_telegram(message)
    sys.exit(0)