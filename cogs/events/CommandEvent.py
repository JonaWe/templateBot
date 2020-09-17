import discord
from discord.ext import commands


class CommandEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.total_executed_commands += 1


def setup(bot):
    bot.add_cog(CommandEvent(bot))
