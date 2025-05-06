from os import listdir, path
from time import sleep
import getpass
import json


downloads_path = path.expanduser("~/Downloads")
json_path = f"/var/db/selfspy/dmgs/{getpass.getuser()}.json"

while True:
    with open(json_path, "w") as f:
        json.dump(list(
            map(lambda x: path.join(downloads_path, x),
                filter(lambda x: x.endswith(".dmg"),
                    listdir(downloads_path)
                    )
                )
            ),
            f
        )
    
    sleep(3)
