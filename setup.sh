#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Пожалуйста, запустите скрипт с sudo"
  if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    return 1
  else
    exit 1
  fi
fi

CURRENT_DIR=$(pwd)
PLIST_PATH="/Library/LaunchDaemons/com.althgamer.selfspy.plist"
LOG_DIR="/var/log"
VENV_PATH="$CURRENT_DIR/venv"
ENV_FILE="$CURRENT_DIR/.env"
PYTHON_BIN="$VENV_PATH/bin/python3"
MAIN_SCRIPT="$CURRENT_DIR/src/main.py"

if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"
if [ -f "$REQUIREMENTS_FILE" ]; then
    "$PYTHON_BIN" -m pip install --upgrade pip
    "$PYTHON_BIN" -m pip install -r "$CURRENT_DIR/requirements.txt"
fi

if [ ! -f "$ENV_FILE" ]; then
    read -p "Введите TG_BOT_TOKEN: " TG_BOT_TOKEN
    read -p "Введите TG_CHAT_ID: " TG_CHAT_ID
    echo "TG_BOT_TOKEN=$TG_BOT_TOKEN" > "$ENV_FILE"
    echo "TG_CHAT_ID=$TG_CHAT_ID" >> "$ENV_FILE"
fi

sudo tee "$PLIST_PATH" > /dev/null <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.althgamer.selfspy</string>

        <key>ProgramArguments</key>
        <array>
            <string>$PYTHON_BIN</string>
            <string>$MAIN_SCRIPT</string>
        </array>

        <key>RunAtLoad</key>
        <true/>

        <key>KeepAlive</key>
        <true/>

        <key>StandardOutPath</key>
        <string>$LOG_DIR/selfspy.log</string>

        <key>StandardErrorPath</key>
        <string>$LOG_DIR/selfspy_error.log</string>

        <key>UserName</key>
        <string>root</string>
    </dict>
</plist>
EOF

sudo chmod 644 "$PLIST_PATH"
sudo chown root:wheel "$PLIST_PATH"

GROUP_NAME="selfspy"

if ! getent group "$GROUP_NAME" >/dev/null; then
  groupadd "$GROUP_NAME"
fi

usermod -aG "$GROUP_NAME" "$SUDO_USER"
usermod -aG "$GROUP_NAME" root

chown -R $SUDO_USER:"$GROUP_NAME" "$CURRENT_DIR"

sudo launchctl load "$PLIST_PATH"
echo "LaunchDaemon com.althgamer.selfspy загружен."
