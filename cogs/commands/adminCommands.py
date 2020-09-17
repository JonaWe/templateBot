import discord
from discord.ext import commands
import json_helper


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.group()
    @commands.is_owner()
    async def blacklist(self, ctx: discord.ext.commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand!!!")

    @blacklist.command(description="Blacklists users form the bot")
    async def add(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        """
        Blacklists users from thr bot. The blacklisted users cannot use any commands from this bot.
        """
        self.bot.blacklisted_users.append(user.id)

        data = json_helper.read_json("blacklist")
        data["commandBlacklistedUsers"].append(user.id)
        json_helper.write_json("blacklist", data)

        await ctx.send(f"{user.display_name} has been added to the blacklist.")

    @blacklist.command(description="Removes users from the blacklist for this bot")
    async def remove(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        """
        Removes users from blacklist for bot commands.
        """
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
        await ctx.send(f"The server prefix has been set to `{prefix}`. To change it again use `{prefix}prefix <prefix>`!")

def setup(bot):
    bot.add_cog(AdminCommands(bot))
