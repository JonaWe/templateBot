import os

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

    @commands.command(name='help',
                      aliases=['h', 'commands', 'command'])
    async def help(self, ctx, cog="1"):
        """
        Help command!
        """
        embed = discord.Embed(colour=self.bot.embed_colour)

        # list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        # removes all the event cogs from cogs list
        for file in os.listdir(f"{self.bot.cwd}/cogs/events"):
            if file.endswith(".py"):
                cogs.remove(str(file[:-3]))

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

            prefix = json_helper.get_prefix(ctx.guild.id, self.bot)

            embed.title = "Available commands!"

            for c in cogs:
                command_list = ""
                for command in self.bot.get_cog(c).walk_commands():
                    # check if command is a subcommand
                    if command.parent is not None:
                        continue

                    # skip hidden commands commands
                    if command.hidden:
                        continue

                    # command description is empty if there is none
                    command_desc = f" - *{command.help}*" if command.help else ""

                    command_list += f"{prefix}**{command.name}**{command_desc}\n"

                command_list += "\uFEFF"
                embed.add_field(name=c, value=command_list, inline=False)

        # checking if the cog argument is a string
        # -> opening a help page for a command
        elif re.search(r"[a-zA-Z]", cog):
            command_found = False

            for c in cogs:
                for command in self.bot.get_cog(c).walk_commands():
                    print(f"{command.name.lower()} : {cog.lower()}")

                    cog_is_alias = False
                    for alias in command.aliases:
                        cog_is_alias |= str(alias.lower()) == str(cog.lower())

                    if str(command.name.lower()) != str(cog.lower()) \
                            and not cog_is_alias:
                        continue

                    command_found = True

                    embed.title = f"Help for '{command.name}'"

                    embed.description = f"*{command.help}*" if command.help else "No description available."

                    prefix = json_helper.get_prefix(ctx.guild.id, self.bot)

                    aliases = f"`{prefix}{command.name}`\n"

                    if len(command.aliases) > 0:
                        for alias in command.aliases:
                            aliases += f"`{prefix}{alias}`\n"

                    embed.add_field(name="Aliases", value=aliases, inline=False)
            if not command_found:
                ctx.send("fd")

        # invalid cog argument
        # the help page does not exist
        else:
            await ctx.send(f"Invalid argument: `{cog}`. Use the `{json_helper.get_prefix(ctx.guild.id, self.bot)}"
                           f"help` command for more info")
            return

        # sending the help embed to the ctx channel
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
