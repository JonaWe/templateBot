import discord
from discord.ext import commands


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")


def setup(bot):
    bot.add_cog(Template(bot))
