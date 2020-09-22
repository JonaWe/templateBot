import asyncio

import discord
from discord.ext import commands
import customErrors.errors

import json_helper


class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.group(description="Turning the devmode on an off",
                    aliases=["dm", "d"])

    @commands.is_owner()
    @commands.bot_has_guild_permissions(send_messages=True)
    async def devmode(self, ctx: discord.ext.commands.context.Context):
        """
        Interaction with the devmode of this bot.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired

    @devmode.command(description="Turns devmode on")
    @commands.is_owner()
    async def on(self, ctx: discord.ext.commands.context.Context):
        """
        Turns the devmode of this bot on so that other users cannot interact with it.
        """
        self.bot.devmode = True
        data = json_helper.read_json("config")
        data["devmode"] = self.bot.devmode
        json_helper.write_json("config", data)
        await ctx.send("```diff\n+ Devmode has been turned on```")


    @devmode.command(description="Turns devmode off")
    @commands.is_owner()
    async def off(self, ctx: discord.ext.commands.context.Context):
        """
        Turns the devmode of this bot off so that other users can interact with it.
        """
        self.bot.devmode = False
        data = json_helper.read_json("config")
        data["devmode"] = self.bot.devmode
        json_helper.write_json("config", data)
        await ctx.send("```diff\n- Devmode has been turned off```")


    @devmode.command(description="Returns the devmode state",
                     aliases=["state", "s"])
    @commands.is_owner()
    async def status(self, ctx: discord.ext.commands.context.Context):
        """
        This command returns the devmode state the bot is currently in.
        """
        if self.bot.devmode:
            await ctx.send("```diff\n+ Devmode is currently turned on```")
        else:
            await ctx.send("```diff\n- Devmode is currently turned off```")

    @commands.group(description="Manage the blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx: discord.ext.commands.context.Context):
        """
        Interaction with the blacklist of this bot.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired

    @blacklist.command(description="Blacklists users form the bot",
                       aliases=["a"])
    async def add(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        """
        Blacklists users from the bot. The blacklisted users cannot use any commands from this bot.
        """
        self.bot.blacklisted_users.append(user.id)
        async with asyncio.Lock():
            data = json_helper.read_json("blacklist")
            data["commandBlacklistedUsers"].append(user.id)
            json_helper.write_json("blacklist", data)

        await ctx.send(f"{user.display_name} has been added to the blacklist.")

    @blacklist.command(description="Removes users from the blacklist for this bot",
                       aliases=["r"])
    async def remove(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        """
        Removes users from blacklist for bot commands.
        """
        if user.id not in self.bot.blacklisted_users:
            await ctx.send(
                f"{user.display_name} was not found in the blacklist and therefore could not be removed from it.")
            return

        self.bot.blacklisted_users.remove(user.id)
        async with asyncio.Lock():
            data = json_helper.read_json("blacklist")
            data["commandBlacklistedUsers"].remove(user.id)
            json_helper.write_json("blacklist", data)

        await ctx.send(f"{user.display_name} has been removed from the blacklist.")

def setup(bot):
    bot.add_cog(OwnerCommands(bot))
