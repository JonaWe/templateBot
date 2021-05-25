import asyncio

import discord
from discord.ext import commands
import json_helper
import customErrors


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    #region Prefix Command

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
        await ctx.send(embed=discord.Embed(
            title=f"The server prefix has been set to `{prefix}`. To change it again use `{prefix}prefix <prefix>`!",
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        ))

    #endregion

    #region Update Commands

    @commands.group(description="Updates channel ids for certain commands")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def update(self, ctx):
        """
        This command updated channel ids for certain commands.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired()

    #region QuoteChannel

    @update.command(name="quote_channel",
                    aliases=["qc"],
                    description="Sets a quote channel for the quote command")
    async def quote_channel(self, ctx: commands.context.Context, channel: discord.TextChannel):
        """
        This command updated the quote channel for this server. You need to provide a channel id for the quote channel.
        """
        channel_ids = self.bot.channel_ids
        channel_ids["quotes"][str(ctx.guild.id)] = channel.id
        await ctx.channel.send(embed=discord.Embed(
            colour=int(self.bot.config["embed-colours"]["default"], 16),
            title=f"I have updated the quote channel to \"{channel.name}\" ({channel.id})!"
        ))
        async with asyncio.Lock():
            json_helper.write_json("channel", channel_ids)

    #endregion

    #endregion

def setup(bot):
    bot.add_cog(AdminCommands(bot))
