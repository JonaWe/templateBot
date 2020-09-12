import discord
import re
import math
from discord.ext import commands
import json_helper


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    """"@commands.command(name='help',
                      aliases=['h', 'commands'],
                      description='Help command!')
    async def help(self, ctx, cog="1"):
        embed = discord.Embed()

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.title = "Available commends!"

        # list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        # remove all the cogs without commands
        cogs.remove("Template")
        cogs.remove("ReactionEvent")
        cogs.remove("MessageEvent")
        cogs.remove("ErrorEvent")

        # check if the cog argument is a number
        # -> opening a specific help page
        if cog.isnumeric():
            total_pages = math.ceil(len(cogs) / 4)
            current_page = int(cog)

            # check for an invalid page number
            if current_page > total_pages or current_page < 1:
                await ctx.send(
                    f"Invalid page number: `{current_page}`. Use a page number between `1` and `{total_pages}`")
                return

        # checking if the cog argument is a string
        # -> opening a help page for a command
        elif re.search(r"[a-zA-Z]", cog):
            pass

        # invalid cog argument
        # the help page does not exist
        else:
            await ctx.send(f"Invalid argument: `{cog}`. Use the `{json_helper.get_prefix(ctx.guild.id, self.bot)}"
                           f"help` command for more info")
            return

        # sending the help embed to the ctx channel
        await ctx.send(embed=embed)"""


def setup(bot):
    bot.add_cog(Help(bot))
