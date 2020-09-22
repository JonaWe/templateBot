import asyncio

import discord
from discord.ext import commands
import json_helper
import customErrors.errors


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.command(description="Changes the bot prefix",
                      aliases=["p"])
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx: discord.ext.commands.context.Context, *, prefix='-'):
        """
        Changes the bot prefix for this server. The prefix is used for all commands for this bot.
        """
        async with asyncio.Lock():
            data = json_helper.read_json("prefixes")
            data[str(ctx.message.guild.id)] = prefix
            json_helper.write_json("prefixes", data)
        await ctx.send(
            f"The server prefix has been set to `{prefix}`. To change it again use `{prefix}prefix <prefix>`!")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
