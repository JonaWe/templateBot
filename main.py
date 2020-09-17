import discord
from discord.ext import commands
import logging
import os
import asyncio
from pathlib import Path

import json_helper

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


def get_prefix(bot1, ctx):
    prefix = json_helper.get_prefix(ctx.guild.id, bot1)
    return commands.when_mentioned_or(prefix)(bot1, ctx)


# bot setup
bot = commands.Bot(command_prefix=get_prefix,
                   owner_id=306139277195083776,
                   help_command=None,
                   case_insensitive=True)

bot.version = 1.0
bot.author_mention = "<@306139277195083776>"
bot.blacklisted_users = []

bot.total_executed_commands = json_helper.read_json("stats")["executed_commands"]

bot.total_user = -1
bot.total_server = -1

bot.cwd = str(Path(__file__).parent)

bot.embed_colour = discord.Colour.gold()
bot.emoji = {"repeat": "\U0001F501"}
bot.DEFAULTPREFIX = '-'


@bot.event
async def on_ready():
    bot.blacklisted_users = json_helper.read_json("blacklist")["commandBlacklistedUsers"]

    print(f"---------\nlogged in as {bot.user}\n---------")


if __name__ == '__main__':
    token = json_helper.read_json("token")["token"]

    # loading the event, command and task cogs
    cog_types = ["events", "commands", "tasks"]
    for cog_type in cog_types:
        for file in os.listdir(f"{bot.cwd}/cogs/{cog_type}"):
            if file.endswith(".py"):
                bot.load_extension(f"cogs.{cog_type}.{file[:-3]}")

    bot.run(token)
