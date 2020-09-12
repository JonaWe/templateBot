import discord
from discord.ext import commands
import logging
import os
import asyncio

import json_helper


# todo watchtogether
# todo skribble
# todo vier gewinnt


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
                   # help_command=None,
                   case_insensitive=True)

bot.version = 1.0
bot.blacklisted_users = []
bot.author_mention = "<@306139277195083776>"
bot.embed_colour = discord.Colour.gold()
bot.emoji = {"repeat": "\U0001F501"}
bot.DEFAULTPREFIX = '-'


@bot.event
async def on_ready():
    bot.blacklisted_users = json_helper.read_json("blacklist")["commandBlacklistedUsers"]

    bot.loop.create_task(status_task())

    print(f"---------\nlogged in as {bot.user}\n---------")


@bot.event
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name=f"on {len(bot.guilds)} servers. Use -help to start!"),
                                  status=discord.Status.online)
        await asyncio.sleep(60)


if __name__ == '__main__':
    cwd = json_helper.get_cwd()
    token = json_helper.read_json("token")["token"]

    # loading event cogs
    for file in os.listdir(f"{cwd}/cogs/events"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.events.{file[:-3]}")

    # loading command cogs
    for file in os.listdir(f"{cwd}/cogs/commands"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.commands.{file[:-3]}")

    bot.run(token)
