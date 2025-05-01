from dotenv import find_dotenv, load_dotenv

from pathlib import Path
from os import environ, path


load_dotenv(find_dotenv())

BASE_DIR = path.join(path.dirname(path.abspath(__file__)), "saved_data")
BACKLOG_PATH = Path(path.join(BASE_DIR, "backlog.json"))
CRON_PATH = Path(path.join(BASE_DIR, "cron.json"))
APPS_PATH = Path(path.join(BASE_DIR, "apps.json"))
DMGS_PATH = Path(path.join(BASE_DIR, "dgms.json"))
TG_BOT_TOKEN = environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = environ.get("TG_CHAT_ID")

state = {}