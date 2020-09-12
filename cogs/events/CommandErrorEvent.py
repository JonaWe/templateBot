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
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send(
                f"You have used this command incorrectly!\nUse `{json_helper.get_prefix(ctx.guild.id, self.bot)}"
                f"help <command>` for more info about this command.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"This command does not exist!\nUse `{json_helper.get_prefix(ctx.guild.id, self.bot)}"
                           f"help` for a list of the available commends.")
        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)

            hour = ""
            minute = ""
            second = ""

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

            # single
            if hour is "" and minute is "":
                wait_msg = second
            elif hour is "" and second is "":
                wait_msg = minute
            elif minute is "" and second is "":
                wait_msg = hour

            # double
            if hour is not "" and minute is not "" and second is "":
                wait_msg = f"{hour} and {minute}"
            elif hour is not "" and second is not "" and minute is "":
                wait_msg = f"{hour} and {second}"
            elif minute is not "" and second is not "" and hour is "":
                wait_msg = f"{minute} and {second}"

            # triple
            if hour is not "" and minute is not "" and second is not "":
                wait_msg = f"{hour}, {minute} and {second}"

            await ctx.send(f"You must wait {wait_msg} to use this command again!")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permissions to use this command.")
        raise error


def setup(bot):
    bot.add_cog(CommandErrorEvent(bot))
