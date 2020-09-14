import discord
from discord.ext import commands
import random

import embed_helper


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.command(aliases=['flip', 'coinflip', 'cf'],
                      ignore_extra=False,
                      description="Flips a coin")
    async def coin(self, ctx: discord.ext.commands.context.Context):
        """
        Flips a coin with the result heads or tails
        """
        await embed_helper.send_coin_flip_embed(ctx.author, ctx, self.bot)

    @commands.command(aliases=['botinfo', 'info'],
                      description="Displays information about this bot")
    # @commands.cooldown(1, 1000, commands.BucketType.user)
    async def stats(self, ctx: discord.ext.commands.context.Context):
        """
        This command displays some stats and information about this bot.
        """
        await embed_helper.send_stats_embed(ctx, self.bot)

    @commands.command(aliases=['roll dice', 'roll', 'rtd'],
                      description="Rolls a dice")
    async def dice(self, ctx: discord.ext.commands.context.Context, *number):
        """
        Rolls a dice from 1-6. If you add a number after the command you can set the dice range.
        """
        if number:
            if number[0].isnumeric():
                max_value = int(number[0])
            else:
                raise discord.ext.commands.BadArgument("Number expected")
        else:
            max_value = 6
        await embed_helper.send_roll_dice_embed(ctx.author, ctx, self.bot, max_value)

    @commands.command(description="Wipes messages in a channel")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def wipe(self, ctx: discord.ext.commands.context.Context, amount=10):
        """
        Wipes the given amount of messages in the channel where the command is executed in. Default amount of wiped messages is 10.
        """
        await ctx.channel.purge(limit=amount + 1)

    @commands.command(name='test',
                      aliases=['t'])
    @commands.cooldown(1, 1*60*60*24, commands.BucketType.user)
    async def born(self, ctx: discord.ext.commands.context.Context):
        await ctx.send("hey")

def setup(bot):
    bot.add_cog(UserCommands(bot))
