import urllib.parse
import urllib.request
from datetime import datetime

from configs import TG_BOT_TOKEN, TG_CHAT_ID
from storage import load_backlog, save_backlog


def send_to_telegram(message):
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
        backlog = load_backlog()
        backlog.append(message)
        save_backlog(backlog)
        return False

def handle_event(event_type, name, url=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    match event_type:
        case "start":
            message = (
                "🚀 *Приложение запущено*\n"
                f"🕒 *Время:* `{timestamp}`\n"
                f"🔹 *Имя приложения:* `{name}`"
            )
        case "stop":
            message = (
                "⛔ *Приложение закрыто*\n"
                f"🕒 *Время:* `{timestamp}`\n"
                f"🔹 *Имя приложения:* `{name}`"
            )
        case "open_url":
            message = (
                "🆕 *Новый URL открыт*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"🌐 *Браузер*: `{name}`\n"
                f"🔗 *URL*: [{urllib.parse.urlparse(url).netloc}]({url})"
                )
        case "close_url":
            message = (
                "❌ *URL закрыт*\n"
                f"🕒 *Время*: `{timestamp}`\n"
                f"🌐 *Браузер*: `{name}`\n"
                f"🔗 *URL*: [{urllib.parse.urlparse(url).netloc}]({url})"
                )

    flush_backlog()
    send_to_telegram(message)


def flush_backlog():
    backlog = load_backlog()
    if not backlog:
        return
    for message in backlog:
        if not send_to_telegram(message):
            break
    else:
        save_backlog([])

def on_startup():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🖥 *Система запущена*\n🕒 *Время:* `{timestamp}`"
    flush_backlog()
    send_to_telegram(message)
    