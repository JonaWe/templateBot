import discord
from discord.ext import commands
from platform import python_version

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
        await ctx.message.delete()
        await embed_helper.send_coin_flip_embed(ctx.author, ctx, self.bot)

    @commands.command(aliases=['botinfo', 'info'],
                      description="Displays information about this bot")
    # @commands.cooldown(1, 1000, commands.BucketType.user)
    async def stats(self, ctx: discord.ext.commands.context.Context):
        """
        This command displays some stats and information about this bot.
        """
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

        embed = discord.Embed(colour=self.bot.config["embed-colour"], title=f"{self.bot.user.name} Stats", description="\uFEFF")

        embed.add_field(name="Total Servers", value=str(self.bot.total_server))
        embed.add_field(name="Total Users", value=str(self.bot.total_user))
        embed.add_field(name="Total Executed Commands", value=str(self.bot.total_executed_commands))
        embed.add_field(name="Bot Version", value=str(self.bot.__version__))
        embed.add_field(name="Running on", value=f"Python {python_version()}")
        embed.add_field(name="Discord.py Version", value=f"{discord.__version__}")
        if mention_owners != "":
            embed.add_field(name="Developer", value=mention_owners)

        await ctx.send(embed=embed)

    @commands.command(aliases=['roll dice', 'roll', 'rtd'],
                      description="Rolls a dice")
    async def dice(self, ctx: discord.ext.commands.context.Context, *number):
        """
        Rolls a dice from 1-6. If you add a number after the command you can set the dice range.
        """
        await ctx.message.delete()
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

    @commands.command(description="Sends bot invite link",
                      ignore_extra=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: discord.ext.commands.context.Context):
        """
        Sends an invite link for this bot, so you can add it to you own server.
        """
        await ctx.send(self.bot.config["bot-invite-link"])

    @commands.command(name='test',
                      ignore_extra=False,
                      aliases=['t'])
    @commands.cooldown(1, 75, commands.BucketType.user)
    @commands.bot_has_guild_permissions(administrator=True, kick_members=True, ban_members=True, manage_roles=True)
    async def test(self, ctx: discord.ext.commands.context.Context):
        await ctx.send("yooooo")


def setup(bot):
    bot.add_cog(UserCommands(bot))
