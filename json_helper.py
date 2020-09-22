import json
from pathlib import Path


def get_cwd():
    return str(Path(__file__).parent)


def read_json(filename):
    with open(f"{get_cwd()}/data/{filename}.json", "r") as file:
        return json.load(file)


def write_json(filename, data):
    with open(f"{get_cwd()}/data/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


def get_prefix(guild_id, bot):
    data = read_json("prefixes")
    if str(guild_id) in data:
        return data[str(guild_id)]
    else:
        return bot.config["default-prefix"]
