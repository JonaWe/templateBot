import discord
from discord.ext import commands
import json_helper
from humanfriendly import format_timespan


class CommandErrorEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ext.commands.context.Context, error):
        is_error_type = lambda e: isinstance(error, e)
        embed = discord.Embed(colour=discord.Colour(0x800000))
        embed.title = "There seemed to be an error while processing your command!"
        # There seemed to be an error while processing your command!
        # embed red and description
        if is_error_type(commands.CommandError):
            if is_error_type(commands.UserInputError):
                if is_error_type(commands.TooManyArguments):
                    embed.description = f"**Error:**```Too many arguments for this command!```"
                    embed.add_field(name="\uFEFF", value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                else:
                    embed.description = f"**Error:**```You have used this command incorrectly!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
            elif is_error_type(commands.CommandNotFound):
                embed.description = f"**Error:**```This command does not exist!```"
                embed.add_field(name="\uFEFF",
                                value=f"Use `{ctx.prefix}help` for a list of all the commands.")
                await ctx.send(embed=embed)
            elif is_error_type(commands.CommandOnCooldown):
                wait_msg = format_timespan(error.retry_after, max_units=4)

                cooldown_type = error.cooldown.type

                if cooldown_type == discord.ext.commands.BucketType.guild:
                    embed.description = f"**Error:**```This command is on cooldown for this server!```" \
                                        f"\nYou must wait **{wait_msg}** to use `{ctx.prefix}{ctx.command}` again!"
                elif cooldown_type == discord.ext.commands.BucketType.channel:
                    embed.description = f"**Error:**```This command is on cooldown for this channel!```" \
                                        f"\nYou must wait **{wait_msg}** to use `{ctx.prefix}{ctx.command}` again!"
                else:
                    embed.description = f"**Error:**```This command is on cooldown for you!```" \
                                        f"\nYou must wait **{wait_msg}** to use `{ctx.prefix}{ctx.command}` again!"

                embed.add_field(name="\uFEFF", value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                await ctx.send(embed=embed)
            elif is_error_type(commands.CheckFailure):
                if is_error_type(commands.NoPrivateMessage):
                    embed.description = f"**Error:**```This command does not work in DM messages!```"
                    embed.add_field(name="\uFEFF", value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.NSFWChannelRequired):
                    embed.description = f"**Error:**```This command must be executed in a NSFW channel!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.MissingPermissions):
                    # todo list permissions
                    embed.description = f"**Error:**```You dont have permissions to use this command!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.BotMissingPermissions):
                    # todo list permissions
                    embed.description = f"**Error:**```I dont have the required permissions to execute this command!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)

        raise error


def setup(bot):
    bot.add_cog(CommandErrorEvent(bot))
