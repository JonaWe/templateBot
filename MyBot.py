import asyncio

import discord
from discord.ext import commands
import os
from pathlib import Path
import json_helper


class MyBot(commands.Bot):
    version = 1.0
    author_mention = "<@306139277195083776>"
    blacklisted_users = json_helper.read_json("blacklist")["commandBlacklistedUsers"]
    total_executed_commands = json_helper.read_json("stats")["executed_commands"]
    invite_link = "https://discord.com/api/oauth2/authorize?client_id=752564236076580994&permissions=8&scope=bot"
    total_user = -1
    total_server = -1
    cwd = str(Path(__file__).parent)
    embed_colour = discord.Colour.gold()
    emoji = {"repeat": "\U0001F501"}
    DEFAULTPREFIX = '-'
    # todo save devmode in a config json file
    devmode = False

    def get_my_prefix(self, bot, ctx):
        if ctx.guild:
            prefix = json_helper.get_prefix(ctx.guild.id, bot)
        else:
            prefix = self.DEFAULTPREFIX
        return prefix

    def __init__(self):
        super().__init__(command_prefix=self.get_my_prefix, owner_id=306139277195083776, help_command=None,
                         case_insensitive=True)

    def run(self, t):
        cog_types = ["events", "commands", "tasks"]
        for cog_type in cog_types:
            for file in os.listdir(f"{self.cwd}/cogs/{cog_type}"):
                if file.endswith(".py"):
                    self.load_extension(f"cogs.{cog_type}.{file[:-3]}")

        super().run(t)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---------\nlogged in as <{self.user}>\n---------")

    async def check_message_reply(self, message, main_instance: bool):
        # ignore messages from the bot itself
        if message.author == self.user:
            return False

        # ignoring messages form users if devmode is turned on
        if self.devmode:
            if not await self.is_owner(message.author):
                # if the methode was run by the main on_message event
                if main_instance:
                    await message.channel.send("```diff\n- The developer only mode is currently turned on! Therefore I will only process messages form the developer(s) of this bot.```")
                return False

        # ignore commands that are not in bot-commands channel
        if isinstance(message.channel, discord.TextChannel) and message.channel.name != "bot-commands":
            return False

        # ignore dm messages
        if isinstance(message.channel, discord.DMChannel):
            pass

        # ignore messages form blacklisted users
        if message.author.id in self.blacklisted_users:
            return False

        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if not await self.check_message_reply(message, True):
            return

        await self.process_commands(message)
