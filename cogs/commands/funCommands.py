import datetime
import json
import discord
import aiohttp
import string
from discord.ext import commands


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    #region Dad-Joke Command

    @commands.command(name="dad-joke",
                      aliases=["dadjoke", "dad"],
                      description="Tells you a random dad joke.")
    async def dad_joke(self, ctx : commands.context.Context):
        joke = await self.get_dad_joke()
        while len(joke) > 255:
            joke = await self.get_dad_joke()

        embed = discord.Embed(
            title=joke,
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"This dad joke was requested by {ctx.author.name}!")
        await ctx.send(embed=embed)

    async def get_dad_joke(self):
        url = "https://icanhazdadjoke.com/"
        header = {"Accept": "text/plain"}
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(url) as response:
                return await response.text()

    #endregion

    #region Yo-Mama-Joke Command

    @commands.command(name="yo-mama",
                      aliases=["yomoma", "mom"],
                      description="Tells you a random yomomma joke.")
    async def mom_joke(self, ctx : commands.context.Context):
        joke = await self.get_mom_joke()
        while len(joke) > 255:
            joke = await self.get_mom_joke()

        embed = discord.Embed(
            title=joke,
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"This yomomma joke was requested by {ctx.author.name}!")
        await ctx.send(embed=embed)


    async def get_mom_joke(self):
        url = "https://api.yomomma.info/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return json.loads(await response.text()).get("joke")

    #endregion

def setup(bot):
    bot.add_cog(FunCommands(bot))