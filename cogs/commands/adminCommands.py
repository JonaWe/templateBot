import discord
from discord.ext import commands
import json_helper
import customErrors.errors


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

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
            await ctx.send(f"{user.display_name} was not found in the blacklist and therefore could not be removed from it.")
            return
        
        self.bot.blacklisted_users.remove(user.id)

        data = json_helper.read_json("blacklist")
        data["commandBlacklistedUsers"].remove(user.id)
        json_helper.write_json("blacklist", data)

        await ctx.send(f"{user.display_name} has been removed from the blacklist.")

    @commands.command(description="Changes the bot prefix")
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx: discord.ext.commands.context.Context, *, prefix='-'):
        """
        Changes the bot prefix for this server. The prefix is used for all commands for this bot.
        """
        data = json_helper.read_json("prefixes")
        data[str(ctx.message.guild.id)] = prefix
        json_helper.write_json("prefixes", data)
        await ctx.send(
            f"The server prefix has been set to `{prefix}`. To change it again use `{prefix}prefix <prefix>`!")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
