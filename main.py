import subprocess
from time import sleep

from tg import handle_event, on_startup


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

def main():
    on_startup()

    previous_apps = set()

    chrome = "Google Chrome"
    previous_chrome_urls = set()

    safari = "Safari"
    previous_safari_urls = set()

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
        

        sleep(1)


if __name__ == "__main__":
    main()
