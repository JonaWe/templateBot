import discord
from discord.ext import commands
import json_helper


class CommandErrorEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ext.commands.context.Context, error):
        is_error_type = lambda e: isinstance(error, e)

        if is_error_type(commands.CommandError):
            if is_error_type(commands.UserInputError):
                if is_error_type(commands.TooManyArguments):
                    await ctx.send(
                        f"Too many arguments for `{ctx.command}`! Use `{ctx.prefix}"
                        f"help {ctx.command}` for more info about this command.")
                else:
                    await ctx.send(
                        f"You have used this command incorrectly! Use `{ctx.prefix}"
                        f"help {ctx.command}` for more info about this command.")
            elif is_error_type(commands.CommandNotFound):
                await ctx.send(f"This command does not exist!\nUse `{ctx.prefix}"
                               f"help` for a list of the available commends.")
            elif is_error_type(commands.CommandOnCooldown):
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)

                day = None
                hour = None
                minute = None
                second = None

                if int(d) is 1:
                    day = f"{int(h)} day"
                elif int(d) >= 2:
                    day = f"{int(h)} days"

                if int(h) is 1:
                    hour = f"{int(h)} hour"
                elif int(h) >= 2:
                    hour = f"{int(h)} hours"

                if int(m) is 1:
                    minute = f"{int(m)} minute"
                elif int(m) >= 2:
                    minute = f"{int(m)} minutes"

                if int(s) is 1:
                    second = f"{int(s)} second"
                elif int(s) >= 2:
                    second = f"{int(s)} seconds"

                wait_msg = ""

                if day:
                    if hour:
                        if minute:
                            if second:
                                wait_msg = f"{day}, {hour}, {minute} and {second}"
                            else:
                                wait_msg = f"{day}, {hour} and {minute}"
                        else:
                            if second:
                                wait_msg = f"{day}, {hour} and {second}"
                            else:
                                wait_msg = f"{day} and {hour}"
                    else:
                        if minute:
                            if second:
                                wait_msg = f"{day}, {minute} and {second}"
                            else:
                                wait_msg = f"{day} and {minute}"
                        else:
                            if second:
                                wait_msg = f"{day} and {second}"
                            else:
                                wait_msg = f"{day}"
                else:
                    if hour:
                        if minute:
                            if second:
                                wait_msg = f"{hour}, {minute} and {second}"
                            else:
                                wait_msg = f"{hour} and {minute}"
                        else:
                            if second:
                                wait_msg = f"{hour} and {second}"
                            else:
                                wait_msg = f"{hour}"
                    else:
                        if minute:
                            if second:
                                wait_msg = f"{minute} and {second}"
                            else:
                                wait_msg = f"{minute}"
                        else:
                            wait_msg = f"{second}"

                await ctx.send(f"You must wait {wait_msg} to use this command again!")
            elif is_error_type(commands.CheckFailure):
                if is_error_type(commands.NoPrivateMessage):
                    await ctx.send("No Private Message")
                elif is_error_type(commands.NSFWChannelRequired):
                    await ctx.send("NSFW channel required")
                elif is_error_type(commands.MissingPermissions):
                    await ctx.send("You lack permissions to use this command")
                elif is_error_type(commands.BotMissingPermissions):
                    await ctx.send("I dont have the required permissions to execute this command")

        raise error


def setup(bot):
    bot.add_cog(CommandErrorEvent(bot))
