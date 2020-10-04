import discord
from discord.ext import commands
import os
from pathlib import Path
import json_helper


def lines_of_file(file):
    return sum(1 for line in open(file))


def get_total_code_lines():
    cwd = json_helper.get_cwd()
    total_lines = 0
    cog_types = ["events", "commands", "tasks"]
    for cog_type in cog_types:
        for file in os.listdir(f"{cwd}/cogs/{cog_type}"):
            if file.endswith(".py"):
                total_lines += lines_of_file(f"{cwd}/cogs/{cog_type}/{file}")

    for file in os.listdir(f"{cwd}"):
        if file.endswith(".py"):
            total_lines += lines_of_file(f"{cwd}/{file}")

    for file in os.listdir(f"{cwd}/customErrors"):
        if file.endswith(".py"):
            total_lines += lines_of_file(f"{cwd}/customErrors/{file}")

    return total_lines

class MyBot(commands.Bot):
    __version__ = 1.0
    blacklisted_users = json_helper.read_json("blacklist")["commandBlacklistedUsers"]
    total_executed_commands = json_helper.read_json("stats")["executed_commands"]
    total_user = "Unknown"
    total_server = "Unknown"
    total_lines_code = get_total_code_lines()
    cwd = str(Path(__file__).parent)
    emoji = {"repeat": "\U0001F501"}
    config = json_helper.read_json("config")


    def get_my_prefix(self, bot, ctx):
        if ctx.guild:
            prefix = json_helper.get_prefix(ctx.guild.id, bot)
        else:
            prefix = self.config["default-prefix"]
        return prefix

    def __init__(self):
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.members = True

        super().__init__(command_prefix=self.get_my_prefix, owner_ids=self.config["owner-ids"], help_command=None,
                         case_insensitive=True, intents=intents)

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

        # ignore commands that are not in bot-commands channel
        if isinstance(message.channel, discord.TextChannel) and message.channel.name != "bot-commands":
            return False

        # ignore dm messages
        if isinstance(message.channel, discord.DMChannel):
            pass

        # ignore messages form blacklisted users
        if message.author.id in self.blacklisted_users:
            return False

        # ignoring messages form users if devmode is turned on
        if self.config["devmode"]:
            if not await self.is_owner(message.author):
                # if the methode was run by the main on_message event
                if main_instance:
                    if isinstance(message.channel, discord.TextChannel):
                        pref = json_helper.get_prefix(message.guild.id, self)
                        if message.content.startswith(pref):
                            await message.channel.send("```diff\n- The developer only mode is currently turned on! Therefore I will only process messages form the developer(s) of this bot.```")
                    else:
                        await message.channel.send("```diff\n- The developer only mode is currently turned on! Therefore I will only process messages form the developer(s) of this bot.```")
                return False
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if not await self.check_message_reply(message, True):
            return

        await self.process_commands(message)
