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
    total_user = -1
    total_server = -1
    cwd = str(Path(__file__).parent)
    embed_colour = discord.Colour.gold()
    emoji = {"repeat": "\U0001F501"}
    DEFAULTPREFIX = '-'

    @staticmethod
    def get_my_prefix(bot1, ctx):
        prefix = json_helper.get_prefix(ctx.guild.id, bot1)
        return commands.when_mentioned_or(prefix)(bot1, ctx)

    def __init__(self):
        super().__init__(command_prefix=self.get_my_prefix, owner_id=306139277195083776, help_command=None,
                         case_insensitive=True)
        self.version = 1.0
        self.author_mention = "<@306139277195083776>"
        self.blacklisted_users = json_helper.read_json("blacklist")["commandBlacklistedUsers"]
        self.total_executed_commands = json_helper.read_json("stats")["executed_commands"]
        self.total_user = -1
        self.total_server = -1
        self.cwd = str(Path(__file__).parent)
        self.embed_colour = discord.Colour.gold()
        self.emoji = {"repeat": "\U0001F501"}
        self.DEFAULTPREFIX = '-'

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
