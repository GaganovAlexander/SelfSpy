from dotenv import find_dotenv, load_dotenv

from pathlib import Path
from os import environ, path


load_dotenv(find_dotenv())

BASE_DIR = path.dirname(path.abspath(__file__)) 
BACKLOG_PATH = Path(path.join(BASE_DIR, "backlog.json"))
TG_BOT_TOKEN = environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = environ.get("TG_CHAT_ID")
