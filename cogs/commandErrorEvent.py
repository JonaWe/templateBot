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

            if h is 0 and m is 0:
                wait_msg = f"{int(s)} seconds"
            elif h is 0:
                wait_msg = f"{int(m)} minutes and {int(s)} seconds"
            else:
                wait_msg = f"{int(h)} hour, {int(m)} minutes and {int(s)} seconds"

            await ctx.send(f"You must wait {wait_msg} to use this command again!")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permissions to use this command.")
        raise error


def setup(bot):
    bot.add_cog(ErrorEvent(bot))
