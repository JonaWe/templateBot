import discord
from discord.ext import commands


class SteamCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.command(name="steamstats",
                      description="Displays stats about a steam user")
    async def steam_stats(self, ctx: commands.context.Context, steam64id: int):
        """
        This command displays some stats about a steam user. You need to provide a steam64id for this command
        """
        pass


    @commands.command(name="csgostats",
                      description="Displays csgo stats for a csgo player")
    async def csgo_stats(self, ctx: commands.context.Context, steam64id: int):
        """
        This command displays some csgo stats for a user. You need to provide a steam64id for this command
        """
        pass


    @commands.command(name="ruststats",
                      description="Displays rust stats for a rust player")
    async def rust_stats(self, ctx: commands.context.Context, steam64id: int):
        """
        This command displays some rust stats for a user. You need to provide a steam64id for this command
        """
        pass


def setup(bot):
    bot.add_cog(SteamCommands(bot))