import json
from pathlib import Path


def get_cwd():
    return str(Path(__file__).parent)


def read_json(filename):
    return json.load(open(f"{get_cwd()}\\data\\{filename}.json", "r"))


def write_json(filename, data):
    json.dump(data, open(f"{get_cwd()}\\data\\{filename}.json", "w"), indent=4)


def get_prefix(guild_id, bot):
    data = read_json("prefixes")
    if str(guild_id) in data:
        return data[str(guild_id)]
    else:
        return bot.DEFAULTPREFIX
