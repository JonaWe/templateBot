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

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """
        Flipps a coin.
        """
        await embed_helper.send_coin_flip_embed(ctx.author, ctx, self.bot)

    @commands.command(aliases=['botinfo', 'info'])
    # @commands.cooldown(1, 1000, commands.BucketType.user)
    async def stats(self, ctx):
        """
        Displays stats about this bot.
        """
        await embed_helper.send_stats_embed(ctx, self.bot)

    @commands.command(aliases=['roll dice', 'roll'])
    async def dice(self, ctx, *number):
        """
        Rolls a dice from 1-6. If you add a number after the command you can set the dice range.
        """
        if number:
            if number[0].isnumeric():
                max_value = int(number[0])
            else:
                await ctx.send("Enter a fucking number u stupid shit")
        else:
            max_value = 6
        await embed_helper.send_roll_dice_embed(ctx.author, ctx, self.bot, max_value)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def wipe(self, ctx, amount=10):
        """
        Wipes the given amount of messages.
        """
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 30, type=commands.BucketType.guild)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.has_guild_permissions(move_members=True)
    async def shuffle(self, ctx):
        source_channel = self.bot.get_channel(int(536968824751390741))
        team1_channel = self.bot.get_channel(int(536969317431115776))
        team2_channel = self.bot.get_channel(int(536969336263278592))

        members_in_source = source_channel.members

        # shuffling the members in source channel
        random.shuffle(members_in_source)

        # splitting the members of the source channel in 2 lists
        team1_members = members_in_source[:len(members_in_source)//2]
        team2_members = members_in_source[len(members_in_source)//2:]

        for user in team1_members:
            await user.move_to(team1_channel)

        for user in team2_members:
            await user.move_to(team2_channel)

        for i in range(len(team1_members)):
            team1_members[i] = team1_members[i].name

        for i in range(len(team2_members)):
            team2_members[i] = team2_members[i].name

        await ctx.send(f"Team 1:{str(team1_members)}\n"
                       f"Team 2:{str(team2_members)}")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.has_guild_permissions(move_members=True)
    async def unshuffle(self, ctx):
        source_channel = self.bot.get_channel(int(536968824751390741))
        team1_channel = self.bot.get_channel(int(536969317431115776))
        team2_channel = self.bot.get_channel(int(536969336263278592))

        for user in team1_channel.members:
            await user.move_to(source_channel)

        for user in team2_channel.members:
            await user.move_to(source_channel)
        # member = ctx.guild.get_member(306139277195083776)

def setup(bot):
    bot.add_cog(UserCommands(bot))
