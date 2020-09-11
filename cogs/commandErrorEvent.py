import discord
from discord.ext import commands
import json_helper


class ErrorEvent(commands.Cog):
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

            wait_msg = ""

            if int(h) is 1:
                wait_msg += f"{int} hour, "
            elif int(h) >= 2:
                wait_msg += f"{int} hours, "

            if int(m) is 1:
                wait_msg += f"{int} minute, "
            elif int(m) >= 2:
                wait_msg += f"{int} minutes, "

            if int(s) is 1:
                wait_msg += f"{int} second"
            elif int(s) >= 2:
                wait_msg += f"{int} seconds"
            elif len(wait_msg) >= 2:
                if wait_msg[len(wait_msg) - 2:] is "":
                    wait_msg = wait_msg[len(wait_msg) - 2:]

            await ctx.send(f"You must wait {wait_msg} to use this command again!")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permissions to use this command.")
        raise error


def setup(bot):
    bot.add_cog(ErrorEvent(bot))
