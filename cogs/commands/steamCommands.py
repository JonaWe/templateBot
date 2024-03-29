import json
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands


class SteamCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_token = self.bot.token["steam"]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    # region Steamstats Command

    @commands.command(name="steamstats",
                      description="Displays stats about a steam user",
                      hidden=True)
    async def steam_stats(self, ctx: commands.context.Context, steam64id: int):
        """
        This command displays some stats about a steam user. You need to provide a steam64id for this command
        """
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.api_token}&steamids={steam64id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    payload = json.loads(await response.text())
                    user = payload["response"]["players"][0]

                    name = user["personaname"]
                    profile_url = user["profileurl"]
                    avatar_url = user["avatarfull"]
                    avatar_small_url = user["avatar"]

                    embed = discord.Embed(
                        colour=int(self.bot.config["embed-colours"]["default"], 16),
                        title=f"'{name}'",
                        url=profile_url
                    )
                    embed.set_thumbnail(url=avatar_url)
                    embed.set_author(name=f"{name}'s steam stats", icon_url=avatar_small_url)

                    # check if the profile is private
                    if user["communityvisibilitystate"] != 3:
                        embed.description = "I cannot grab any info about this steam user because their profile is not public!"

                        await ctx.send(embed=embed)

                    # profile is public
                    else:
                        time_created = datetime.utcfromtimestamp(user["timecreated"]).strftime('%Y-%m-%d %H:%M:%S')

                        status = user["personastateflags"]
                        embed.add_field(name="Time created", value=time_created, inline=False)

                        await ctx.send(embed=embed)

    # endregion

    # region Csgostats Command

    @commands.command(name="csgostats",
                      description="Displays csgo stats for a csgo player",
                      hidden=True)
    async def csgo_stats(self, ctx: commands.context.Context, steam64id: int):
        """
        This command displays some csgo stats for a user. You need to provide a steam64id for this command
        """
        pass

    # endregion

    # region Ruststats Command

    @commands.command(name="ruststats",
                      description="Displays rust stats for a rust player",
                      hidden=True)
    async def rust_stats(self, ctx: commands.context.Context, steam64id: int):
        """
        This command displays some rust stats for a user. You need to provide a steam64id for this command
        """
        pass

    # endregion


def setup(bot):
    bot.add_cog(SteamCommands(bot))
