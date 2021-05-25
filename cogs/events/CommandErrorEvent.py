import discord
from discord.ext import commands
from humanfriendly import format_timespan

import customErrors.errors


class CommandErrorEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ext.commands.context.Context, error):
        is_error_type = lambda e: isinstance(error, e)
        embed = discord.Embed(colour=int(self.bot.config["embed-colours"]["error"], 16))
        embed.title = "There seemed to be an error while processing your command!"

        if is_error_type(commands.CommandError):
            if is_error_type(commands.UserInputError):
                if is_error_type(commands.TooManyArguments):
                    embed.description = f"**Error:**```fix\nToo many arguments for this command!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.BadArgument):
                    if is_error_type(commands.MessageNotFound):
                        embed.description = f"**Error:**```fix\nI could not find the message!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.MemberNotFound):
                        embed.description = f"**Error:**```fix\nI could not find the member!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.UserNotFound):
                        embed.description = f"**Error:**```fix\nI could not find the user!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.ChannelNotFound):
                        embed.description = f"**Error:**```fix\nI could not find the channel!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.ChannelNotReadable):
                        embed.description = f"**Error:**```fix\nThe channel is not readable for me!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.BadColourArgument):
                        embed.description = f"**Error:**```fix\nThe colour is invalid!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.RoleNotFound):
                        embed.description = f"**Error:**```fix\nI could not find the role!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.EmojiNotFound):
                        embed.description = f"**Error:**```fix\nI could not find the emoji!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(commands.BadBoolArgument):
                        embed.description = f"**Error:**```fix\nThat is not a valid boolean!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    elif is_error_type(customErrors.errors.SubCommandRequired):
                        embed.description = f"**Error:**```fix\nA subcommand is required in order to run this command!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                    else:
                        embed.description = f"**Error:**```fix\nInvalid argument for this command!```"
                        embed.add_field(name="\uFEFF",
                                        value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                        await ctx.send(embed=embed)
                elif is_error_type(customErrors.errors.NoPermissionsToViewThisCommand):
                    embed.description = f"**Error:**```fix\nYou do not have permissions to view this command!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(customErrors.errors.CogDoesNotExist):
                    embed.description = f"**Error:**```fix\nThis cog does not exist!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                else:
                    embed.description = f"**Error:**```fix\nYou have used this command incorrectly!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
            elif is_error_type(commands.CommandNotFound):
                embed.description = f"**Error:**```fix\nThis command does not exist!```"
                embed.add_field(name="\uFEFF",
                                value=f"Use `{ctx.prefix}help` for a list of all the commands.")
                await ctx.send(embed=embed)
            elif is_error_type(commands.CommandOnCooldown):
                wait_msg = format_timespan(error.retry_after, max_units=4)

                cooldown_type = error.cooldown.type

                if cooldown_type == discord.ext.commands.BucketType.guild:
                    embed.description = f"**Error:**```fix\nThis command is on cooldown for this server!```" \
                                        f"\nYou must wait **{wait_msg}** to use `{ctx.prefix}{ctx.command}` again!"
                elif cooldown_type == discord.ext.commands.BucketType.channel:
                    embed.description = f"**Error:**```fix\nThis command is on cooldown for this channel!```" \
                                        f"\nYou must wait **{wait_msg}** to use `{ctx.prefix}{ctx.command}` again!"
                else:
                    embed.description = f"**Error:**```fix\nThis command is on cooldown for you!```" \
                                        f"\nYou must wait **{wait_msg}** to use `{ctx.prefix}{ctx.command}` again!"

                embed.add_field(name="\uFEFF",
                                value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                await ctx.send(embed=embed)
            elif is_error_type(commands.CommandInvokeError):
                owner = []
                if self.bot.owner_ids:
                    for o in self.bot.owner_ids:
                        owner.append(o)
                elif self.bot.owner_id:
                    owner.append(self.bot.owner_id)

                mention_owners = ""
                if len(owner) > 0:
                    for o in owner:
                        mention_owners += f"<@{o}>\n"

                embed.description = f"**Error:**```fix\nAn unexpected error occurred!```"
                embed.add_field(name="\uFEFF",
                                value=f"Please report the error the the author of the bot:\n{mention_owners}")
                await ctx.send(embed=embed)
            elif is_error_type(commands.CheckFailure):
                if is_error_type(commands.NoPrivateMessage):
                    embed.description = f"**Error:**```fix\nThis command does not work in DM messages!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.NSFWChannelRequired):
                    embed.description = f"**Error:**```fix\nThis command must be executed in a NSFW channel!```"
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.MissingPermissions):
                    embed.description = f"**Error:**```fix\nYou dont have permissions to use this command!```"

                    # getting the missing permission(s) in order to execute the command
                    missing_permissions = [f"`{per.capitalize()}`" for per in error.missing_perms]
                    name = "Missing Permissions" if len(missing_permissions) > 1 else "Missing Permission"
                    if len(missing_permissions) > 2:
                        missing_permissions = f"{', '.join(missing_permissions[:-1])} and {missing_permissions[-1]}"
                    else:
                        missing_permissions = " and ".join(missing_permissions)
                    embed.add_field(name=name, value=missing_permissions, inline=False)

                    # adding the help field
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)
                elif is_error_type(commands.BotMissingPermissions):
                    embed.description = f"**Error:**```fix\nI dont have the required permissions to execute this command!```"

                    # getting the missing permission(s) in order to execute the command
                    missing_permissions = [f"`{per.capitalize()}`" for per in error.missing_perms]
                    name = "Missing Permissions" if len(missing_permissions) > 1 else "Missing Permission"
                    if len(missing_permissions) > 2:
                        missing_permissions = f"{', '.join(missing_permissions[:-1])} and {missing_permissions[-1]}"
                    else:
                        missing_permissions = " and ".join(missing_permissions)
                    embed.add_field(name=name, value=missing_permissions, inline=False)

                    # adding the help field
                    embed.add_field(name="\uFEFF",
                                    value=f"Use `{ctx.prefix}help {ctx.command}` for more information about this command.")
                    await ctx.send(embed=embed)

        raise error


def setup(bot):
    bot.add_cog(CommandErrorEvent(bot))
