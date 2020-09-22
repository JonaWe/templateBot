import os

import discord
from discord.ext import commands
from humanfriendly import format_timespan
import customErrors.errors


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

        # converts command tuple to string
        command = " ".join(command)

        # check if the command argument is empty
        # -> opening the global help page
        if command  == "":
            embed = discord.Embed(colour=self.bot.config["embed-colour"])

            embed.title = "Available commands!"

            # list of all cogs
            cogs = [c for c in self.bot.cogs.keys()]

            # removes all the cogs with no commands
            remove_cogs = ["events", "tasks"]
            for remove_cog in remove_cogs:
                for file in os.listdir(f"{self.bot.cwd}/cogs/{remove_cog}"):
                    if file.endswith(".py"):
                        cogs.remove(str(file[:-3]))

            for c in cogs:
                cog = self.bot.get_cog(c)

                # skipping the owner commands cog if the user is not an owner
                if cog.qualified_name == "OwnerCommands" and not await self.bot.is_owner(ctx.author):
                    continue

                command_list = ""
                for command in cog.walk_commands():
                    # check if command is a subcommand to only display top level commands
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

            embed.add_field(name="\uFEFF", value=f"Use `{ctx.prefix}help <command>` to get more information about a command.")

            # sending the help message and ending the function
            await ctx.send(embed=embed)
            return

        # help command for a specific command
        else:
            # getting the command object from the bot (including subcommands)
            command = self.bot.get_command(command)

            if command is None:
                raise discord.ext.commands.BadArgument("Invalid command passed for the help command")

            # check if the commands belongs to a cog
            if command.cog is not None:
                # raising an error if the command is an owner command an the user is not an owner
                if command.cog.qualified_name == "OwnerCommands" and not await self.bot.is_owner(ctx.author):
                    raise customErrors.errors.NoPermissionsToViewThisCommand()

            embed = discord.Embed(colour=self.bot.config["embed-colour"])

            # getting the name of the parent commands
            full_parent_name = command.full_parent_name + " " if command.full_parent_name != "" else ""
            full_name = full_parent_name + command.name

            embed.title = f"Help for the **{full_name}** command"

            # if no help text is defined for the command the description text will be taken instead
            description = f"*{command.help}*" if command.help else command.description
            embed.description = description if description else "No description available."

            # adding command usage example to the description
            embed.description += f"\n```{ctx.prefix}{full_name}"
            if command.clean_params:
                parameters = list(command.clean_params)
                for parameter in parameters:
                    embed.description += f" <{str(parameter)}>"
            embed.description += "```"

            # adding aliases field if aliases exist for this command
            if len(command.aliases) > 0:
                aliases = ""
                for alias in command.aliases:
                    aliases += f"`{ctx.prefix}{full_parent_name}{alias}`\n"
                embed.add_field(name="Aliases", value=aliases, inline=False)

            # adding subcommand field
            if isinstance(command, discord.ext.commands.Group):
                sub_commands = []
                for sc in command.walk_commands():
                    if sc.hidden:
                        continue
                    if sc.parent is not command:
                        continue
                    sub_commands.append(f"`{sc.name}`")
                if len(sub_commands) > 0:
                    embed.add_field(name="Subcommands", value="\n".join(sub_commands))

            # adding cooldown field if a cooldown is active for the command
            if command._buckets._cooldown:
                rate_string = f"{command._buckets._cooldown.rate} times" if command._buckets._cooldown.rate > 1 else f"{command._buckets._cooldown.rate} time"
                per_string = format_timespan(command._buckets._cooldown.per, max_units=3)

                types = {discord.ext.commands.BucketType.user: "user",
                         discord.ext.commands.BucketType.guild: "server",
                         discord.ext.commands.BucketType.channel: "channel",
                         discord.ext.commands.BucketType.member: "member",
                         discord.ext.commands.BucketType.role: "role",
                         discord.ext.commands.BucketType.category: "category",
                         discord.ext.commands.BucketType.default: "default",
                         }
                msg_content = f"This command can be used **{rate_string}** every **{per_string}** per **{types.get(command._buckets._cooldown.type, '<unknown>')}**."
                embed.add_field(name="**Cooldown**", value=msg_content)

            # sending the help message
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
