from pathlib import Path
import json


CONFIG_FILE = Path("config.json")


DEFAULT_CONFIG = {
    "image_provider": "pollinations"
}


def load_config():

    if not CONFIG_FILE.exists():

        save_config(DEFAULT_CONFIG)

    with open(CONFIG_FILE, "r") as file:

        return json.load(file)


def save_config(config):

    with open(CONFIG_FILE, "w") as file:

        json.dump(config, file, indent=4)