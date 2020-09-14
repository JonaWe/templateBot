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
                      description='Help command',
                      aliases=['h', 'commands', 'command'])
    async def help(self, ctx: discord.ext.commands.context.Context, *command):
        """
        Use the help command to get a list of all the available command. If you want to know more about a command use the help command with the other command as an parameter.
        """

        # raising error when more than one argument is found
        if len(command) > 1:
            raise discord.ext.commands.TooManyArguments(f"One argument was expected. Instead found {len(command)} arguments")

        # list of all cogs
        cogs = [c for c in self.bot.cogs.keys()]

        # removes all the cogs with no commands
        remove_cogs = ["events", "tasks"]
        for remove_cog in remove_cogs:
            for file in os.listdir(f"{self.bot.cwd}/cogs/{remove_cog}"):
                if file.endswith(".py"):
                    cogs.remove(str(file[:-3]))

        # check if the cog argument is a number
        # -> opening a specific help page
        if not command:
            embed = discord.Embed(colour=self.bot.embed_colour)

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
                    command_desc = f" - *{command.description}*" if command.description else ""

                    command_list += f"{ctx.prefix}**{command.name}**{command_desc}\n"

                command_list += "\uFEFF"
                embed.add_field(name=c, value=command_list, inline=False)

            # sending the help message and ending the function
            await ctx.send(embed=embed)
            return

        elif re.search(r"[a-zA-Z]", str(command)):
            cog = command[0]
            command_found = False

            for c in cogs:
                for command in self.bot.get_cog(c).walk_commands():
                    cog_is_alias = False
                    for alias in command.aliases:
                        cog_is_alias |= str(alias.lower()) == str(cog.lower())

                    if str(command.name.lower()) != str(cog.lower()) \
                            and not cog_is_alias:
                        continue

                    command_found = True

                    embed = discord.Embed(colour=self.bot.embed_colour)

                    embed.title = f"Help for the **{command.name}** command"

                    # if no help text is defined for the command the description text will be taken instead
                    description = f"*{command.help}*" if command.help else command.description
                    embed.description = description if description else "No description available."

                    aliases = f"`{ctx.prefix}{command.name}`\n"

                    if len(command.aliases) > 0:
                        for alias in command.aliases:
                            aliases += f"`{ctx.prefix}{alias}`\n"

                    embed.add_field(name="Aliases", value=aliases, inline=True)

                    if command.clean_params:
                        parameters = list(command.clean_params)
                        parameter_string = ""
                        for parameter in parameters:
                            parameter_string += f"<{str(parameter)}> "
                        embed.add_field(name="Parameter", value=parameter_string, inline=False)


                    # sending the help message
                    await ctx.send(embed=embed)

            if not command_found:
                raise discord.ext.commands.BadArgument("Invalid command passed for the help command")
            else:
                return

        await ctx.send(f"**An unexpected error occurred!** Please contact {self.bot.author_mention} "
                       f"with the following error code: `helpCommand.py exception`.")


def setup(bot):
    bot.add_cog(Help(bot))
