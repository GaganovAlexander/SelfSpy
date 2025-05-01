import subprocess
from os import listdir, path
from time import sleep
import signal

from storage import load_cron, load_apps, load_dmgs
from tg import handle_event, on_startup, on_shutdown
from configs import state


def get_active_windows():
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
    crontabs = listdir("/var/at/tabs")
    crontasks = {}
    for tab in crontabs:
        crontasks[tab] = subprocess.run(
            ["crontab", "-u", tab, "-l"],
            capture_output=True, text=True
            ).stdout.strip().split("\n")
    return crontasks

def get_applications():
    result = listdir("/Applications")
    return set(map(lambda x: x.removesuffix(".app"), result))

def get_dmgs():
    result = set()
    for user in listdir("/Users"):
        downloads_path = f"/Users/{user}/Downloads"
        if path.isdir(downloads_path):
            for file in listdir(downloads_path):
                if file.endswith(".dmg"):
                    full_path = path.join(downloads_path, file)
                    result.add(full_path.removesuffix(".dmg"))
    return result
        

current_crontasks = {}
def main():
    previous_windows= set()

    chrome = "Google Chrome"
    previous_chrome_urls = set()

    safari = "Safari"
    previous_safari_urls = set()

    previous_crontasks = load_cron()
    previous_apps = load_apps()
    previous_dmgs = load_dmgs()

    while True:
        # Блок с проверкой приложений
        current_windows = get_active_windows()
        new_windows = current_windows - previous_windows
        closed_windows = previous_windows - current_windows
        previous_windows = current_windows

        for window in new_windows:
            handle_event("start", window)
        for window in closed_windows:
            handle_event("stop", window)
        

        # Блок с проверкой вкладок браузера
        if chrome in current_windows:
            chrome_urls = get_active_tabs(chrome)
            new_chrome_urls = chrome_urls - previous_chrome_urls
            closed_chrome_urls = previous_chrome_urls - chrome_urls
            previous_chrome_urls = chrome_urls

            for url in new_chrome_urls:
                handle_event("open_url", chrome, url)
            for url in closed_chrome_urls:
                handle_event("close_url", chrome, url)

        if safari in current_windows:
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


        # Блок с установкой/удалением приложениями
        state["apps"] = get_applications()
        new_apps = state["apps"] - previous_apps
        deleted_apps = previous_apps - state["apps"]

        for app in new_apps:
            handle_event("installed", app)
        for app in deleted_apps:
            handle_event("uninstalled", app)
        previous_apps = state["apps"]


        # Блок с загрузкой .dmg
        state["dmgs"] = get_dmgs()
        new_dmgs = state["dmgs"] - previous_dmgs

        for dmg in new_dmgs:
            handle_event("downloaded_dmg", dmg)
        previous_dmgs = state["dmgs"]

        sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_shutdown)
    on_startup()
    main()
