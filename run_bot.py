import logging
import json_helper
from MyBot import MyBot

# todo watchtogether
# todo skribble
# todo vier gewinnt
# todo translate
# todo update api python -m pip install -U git+https://github.com/Rapptz/discord.py@master#egg=discord.py[voice]


# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == "__main__":
    bot = MyBot()
    bot.run(json_helper.read_json("token")["token"])