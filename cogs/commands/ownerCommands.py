import asyncio

import discord
from discord.ext import commands
import customErrors.errors
from json import loads
from ast import literal_eval
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
        self.bot.config["devmode"] = True
        json_helper.write_json("config", self.bot.config)
        await ctx.send("```diff\n+ Devmode has been turned on```")

    @devmode.command(description="Turns devmode off")
    @commands.is_owner()
    async def off(self, ctx: discord.ext.commands.context.Context):
        """
        Turns the devmode of this bot off so that other users can interact with it.
        """
        self.bot.config["devmode"] = False
        json_helper.write_json("config", self.bot.config)
        await ctx.send("```diff\n- Devmode has been turned off```")

    @devmode.command(description="Returns the devmode state",
                     aliases=["state", "s"])
    @commands.is_owner()
    async def status(self, ctx: discord.ext.commands.context.Context):
        """
        This command returns the devmode state the bot is currently in.
        """
        if self.bot.config["devmode"]:
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

    @commands.group(description="Manage the config",
                    aliases=["c"])
    @commands.is_owner()
    async def config(self, ctx: discord.ext.commands.context.Context):
        """
        Interaction with the config of this bot.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired

    @config.command(description="Updating values in the config",
                    aliases=['u'])
    async def update(self, ctx: commands.context.Context, variable: str, *value):
        """
        Updating a specific value in the config.
        """
        # turn value argument into string
        value = " ".join(value)

        # if the variable is not in the config an error message will be send
        if variable not in self.bot.config:
            await ctx.send(f"The variable `{variable}` does not exits in the config of the bot! Therefore it was not updated.")
            return

        # if the variable is a string it will be converted to a string else the json converter will handle it
        if isinstance(self.bot.config, str):
            value = str(value)
        else:
            try:
                value = loads(value)
            except:
                raise commands.BadArgument

        # updating the config
        self.bot.config[variable] = value
        json_helper.write_json("config", self.bot.config)
        await ctx.send(f"Successfully updated `{variable}` to `{value}`.")

    @config.command(description="Reloads the config",
                    aliases=['r'])
    async def reload(self, ctx: commands.context.Context):
        """
        Reloads the config file into the bot instance.
        """
        self.bot.config = json_helper.read_json("config")
        await ctx.send("Successfully reloaded the config!")


    @commands.command(description="Converts hex to integer",
                      aliases=['hti'])
    @commands.is_owner()
    async def hextoint(self, ctx: commands.context.Context, hexnumber: str):
        """
        Converts a hexadecimal number into an integer.
        """
        try:
            num = int(hexnumber, 16)
            await ctx.send(f"Converted the hex number `{str(hexnumber)}` to the integer `{str(num)}`.")
        except:
            raise commands.BadArgument()

def setup(bot):
    bot.add_cog(OwnerCommands(bot))
