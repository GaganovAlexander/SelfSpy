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

if ! dscl . -read /Groups/"$GROUP_NAME" &>/dev/null; then
  sudo dseditgroup -o create "$GROUP_NAME"
fi

sudo mkdir /var/db/selfspy
sudo mkdir /var/db/selfspy/dmgs
chmod -R a+rx "$VENV_PATH/bin" 


AGENT_USERS=()
for user_home in /Users/*; do
  username=$(basename "$user_home")
  downloads_dir="$user_home/Downloads"
  if [ -d "$downloads_dir" ]; then
    AGENT_USERS+=("$username")
  fi
done

for user in "${AGENT_USERS[@]}"; do
  username=$(basename "$user_home")
  downloads_dir="$user_home/Downloads"
  echo "Устанавливаю агент для пользователя: $username"
  sudo ./setup_agent.sh "$username"
done


sudo dseditgroup -o edit -a "$SUDO_USER" -t user "$GROUP_NAME"
sudo dseditgroup -o edit -a root -t user "$GROUP_NAME"

chown -R $SUDO_USER:"$GROUP_NAME" "$CURRENT_DIR"

sudo launchctl load "$PLIST_PATH"
echo "LaunchDaemon com.althgamer.selfspy загружен."


{
  echo "#!/bin/bash"
  for user in "${AGENT_USERS[@]}"; do
    uid=$(id -u "$user")
    echo "echo \"Запускаю агент для $user\""
    echo "launchctl bootstrap gui/$uid \"/Users/$user/Library/LaunchAgents/com.althgamer.selfspy.agent.plist\""
  done
  echo ""
  echo "echo \"Запускаю LaunchDaemon\""
  echo "sudo launchctl load /Library/LaunchDaemons/com.althgamer.selfspy.plist"
} | sudo tee ./start.sh > /dev/null

{
  echo "#!/bin/bash"
  for user in "${AGENT_USERS[@]}"; do
    uid=$(id -u "$user")
    echo "echo \"Останавливаю агент для $user\""
    echo "launchctl bootout gui/$uid \"/Users/$user/Library/LaunchAgents/com.althgamer.selfspy.agent.plist\""
  done
  echo ""
  echo "echo \"Останавливаю LaunchDaemon\""
  echo "sudo launchctl unload /Library/LaunchDaemons/com.althgamer.selfspy.plist"
} | sudo tee ./stop.sh > /dev/null

sudo chmod +x ./start.sh ./stop.sh

echo "Скрипты start.sh и stop.sh успешно созданы."
