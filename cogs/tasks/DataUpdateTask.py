import discord
from discord.ext import tasks, commands

import json_helper


class DataUpdateTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_data.start()

    def cog_unload(self):
        self.update_data.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @tasks.loop(seconds=2.0)
    async def update_data(self):
        self.bot.total_server = len(self.bot.guilds)
        self.bot.total_user = len(set(self.bot.get_all_members()))

        data = json_helper.read_json("stats")
        data["executed_commands"] = self.bot.total_executed_commands
        json_helper.write_json("stats", data)

    @update_data.before_loop
    async def wait_function(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(DataUpdateTask(bot))
