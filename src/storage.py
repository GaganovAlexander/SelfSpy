import json

from configs import BACKLOG_PATH, CRON_PATH


def load_backlog():
    if BACKLOG_PATH.exists():
        with open(BACKLOG_PATH, "r") as f:
            return json.load(f)
    return []

def save_backlog(data):
    with open(BACKLOG_PATH, "w") as f:
        json.dump(data, f)
        

def load_cron() -> dict[str, list[str]] | dict:
    if CRON_PATH.exists():
        with open(CRON_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cron(data):
    with open(CRON_PATH, "w") as f:
        json.dump(data, f)
