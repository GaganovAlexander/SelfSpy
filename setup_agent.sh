#!/bin/bash

if [ -z "$1" ]; then
  echo "Использование: sudo ./setup_agent.sh <username>"
  exit 1
fi

USERNAME="$1"
USER_HOME="/Users/$USERNAME"
if [ ! -d "$USER_HOME" ]; then
  echo "Домашняя папка пользователя $USERNAME не найдена"
  exit 1
fi
if [ ! -d "$USER_HOME/Downloads" ]; then 
    echo "У пользователя нет папки Downloads"
    exit 1
fi

AGENT_NAME="com.althgamer.selfspy.agent"
PLIST_NAME="$AGENT_NAME.plist"
AGENT_DIR="$USER_HOME/Library/LaunchAgents"
PLIST_PATH="$AGENT_DIR/$PLIST_NAME"

CURRENT_DIR=$(pwd)
VENV_PATH="$CURRENT_DIR/venv"
PYTHON_BIN="$VENV_PATH/bin/python3"
AGENT_SCRIPT="$CURRENT_DIR/src/agent.py"
LOG_DIR="/var/log"
DB_PATH="/var/db/selfspy/dmgs/$USERNAME.json"
LOG_PATH=$LOG_DIR/selfspy_agent_$USERNAME.log
ERR_LOG_PATH=$LOG_DIR/selfspy_agent_error_$USERNAME.log


sudo -u "$USERNAME" tee "$PLIST_PATH" > /dev/null <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$AGENT_NAME</string>

    <key>ProgramArguments</key>
    <array>
            <string>/usr/bin/python3</string>
            <string>$AGENT_SCRIPT</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>$LOG_PATH</string>

    <key>StandardErrorPath</key>
    <string>$ERR_LOG_PATH</string>
</dict>
</plist>
EOF


sudo chown "$USERNAME":staff "$PLIST_PATH"
sudo chmod 644 "$PLIST_PATH"

sudo touch "$DB_PATH"
sudo chown "$USERNAME":staff "$DB_PATH"
sudo chmod 644 "$DB_PATH"


sudo touch $LOG_PATH
sudo chown "$USERNAME":staff "$LOG_PATH"
sudo chmod 644 "$LOG_PATH"

sudo touch $ERR_LOG_PATH
sudo chown "$USERNAME":staff "$ERR_LOG_PATH"
sudo chmod 644 "$ERR_LOG_PATH"

launchctl bootout gui/$(id -u "$USERNAME") "$PLIST_PATH" &>/dev/null
launchctl bootstrap gui/$(id -u "$USERNAME") "$PLIST_PATH"

echo "LaunchAgent $AGENT_NAME установлен и запущен для пользователя $USERNAME."
