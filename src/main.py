import subprocess
from time import sleep
import signal

from storage import load_cron
from tg import handle_event, on_startup, on_shutdown
from configs import state


def get_active_apps():
    result = subprocess.run(
                    ["osascript", "-e",
                    'tell application "System Events" to get name of every process whose visible is true'],
                    capture_output=True, text=True
                    )
    return set(result.stdout.strip().split(", "))

def get_active_tabs(browser):
    result = subprocess.run(
                    ["osascript", "-e",
                    f'tell application "{browser}" to get URL of tabs of windows'],
                    capture_output=True, text=True
                    )
    return set(result.stdout.strip().split(", "))

def get_crontabs() -> dict[str, list[str]]:
    crontabs = subprocess.run(
                    ["sudo", "ls", "/var/at/tabs"],
                    capture_output=True, text=True
                    ).stdout.strip().split()
    crontasks = {}
    for tab in crontabs:
        crontasks[tab] = subprocess.run(
            ["sudo", "crontab", "-u", tab, "-l"],
            capture_output=True, text=True
            ).stdout.strip().split("\n")
    return crontasks
        
current_crontasks = {}
def main():
    previous_apps = set()

    chrome = "Google Chrome"
    previous_chrome_urls = set()

    safari = "Safari"
    previous_safari_urls = set()

    previous_crontasks = load_cron()

    while True:
        # Блок с проверкой приложений
        current_apps = get_active_apps()
        new_apps = current_apps - previous_apps
        closed_apps = previous_apps - current_apps
        previous_apps = current_apps

        for app in new_apps:
            handle_event("start", app)
        for app in closed_apps:
            handle_event("stop", app)
        

        # Блок с проверкой вкладок браузера
        if chrome in current_apps:
            chrome_urls = get_active_tabs(chrome)
            new_chrome_urls = chrome_urls - previous_chrome_urls
            closed_chrome_urls = previous_chrome_urls - chrome_urls
            previous_chrome_urls = chrome_urls

            for url in new_chrome_urls:
                handle_event("open_url", chrome, url)
            for url in closed_chrome_urls:
                handle_event("close_url", chrome, url)

        if safari in current_apps:
            safari_urls = get_active_tabs(safari)
            new_safari_urls = safari_urls - previous_safari_urls
            closed_safari_urls = previous_safari_urls - safari_urls
            previous_safari_urls = safari_urls

            for url in new_safari_urls:
                handle_event("open_url", safari, url)
            for url in closed_safari_urls:
                handle_event("close_url", safari, url)
        

        # Блок с кронтабами
        state["crontasks"] = get_crontabs()
        for tab in set(state["crontasks"].keys()) | set(previous_crontasks.keys()):
            current_crontasks_set = set(state["crontasks"].get(tab, []))
            previous_crontasks_set = set(previous_crontasks.get(tab, []))

            new_crontasks = current_crontasks_set - previous_crontasks_set
            deleted_crontasks = previous_crontasks_set - current_crontasks_set

            for task in new_crontasks:
                handle_event("new_cron", tab, task)
            for task in deleted_crontasks:
                handle_event("deleted_cron", tab, task)
        previous_crontasks = state["crontasks"]


        sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_shutdown)
    on_startup()
    main()
