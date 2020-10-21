import discord
from discord.ext import commands
from platform import python_version
from games import four_connect
import customErrors

import embed_helper


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.group(description="Managing a four connect game",
                      aliases=["fc"])
    @commands.guild_only()
    async def fourconnent(self, ctx):
        """
        With this command you can manage your four connect game.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired()

    @fourconnent.command(description="Ends a four connect game",
                         aliases=["e", "stop", "exit"])
    async def end(self, ctx: commands.context.Context):
        """
        This commands ends your current four connect game.
        """
        if f"{ctx.author.id}" in self.bot.active_games:
            await ctx.send(embed=discord.Embed(
                colour=int(self.bot.config["embed-colours"]["default"], 16),
                title="I have stopped your four connect game!"
            ))
            self.bot.active_games.pop(str(ctx.author.id))
        else:
            await ctx.send(embed=discord.Embed(
                colour=int(self.bot.config["embed-colours"]["warning"], 16),
                title="You are not playing four connect!"
            ))


    @fourconnent.command(description="Starts a four connect game",
                      aliases=["s"])
    async def start(self, ctx: commands.context.Context, user: discord.Member):
        """
        This command creates a new four connect game between you and another given user.
        """
        # check if the user is the author itself
        if ctx.author == user:
            await ctx.send(embed=discord.Embed(
                colour=int(self.bot.config["embed-colours"]["warning"], 16),
                title="You cannot play against yourself!"
            ))
            return

        # ignoring the command if the user already has a game in progress
        if f"{ctx.author.id}" in self.bot.active_games:
            await ctx.send(embed=discord.Embed(
                colour=int(self.bot.config["embed-colours"]["warning"], 16),
                title="You already have a game in progress!"
            ))
            return


        game = four_connect.Game()
        embed = discord.Embed()
        embed.title = f"Four Connect Game"
        embed.description = f"{ctx.author.mention} has challenged {user.mention} to play four connect."
        embed.set_footer(text="Reply with the checkmark to accept the game invite.")
        embed.colour = int(self.bot.config["embed-colours"]["default"], 16)

        message = await ctx.send(embed=embed, content=str(user.mention))

        await message.add_reaction("\U00002705")

        self.bot.active_games[f"{ctx.author.id}"] = {
            "accepted": False,
            "started": 0,
            "player": ctx.author,
            "enemy": user,
            "game": game,
            "embed": embed,
            "message": message
        }





    @commands.command(aliases=['flip', 'coinflip', 'cf'],
                      ignore_extra=False,
                      description="Flips a coin")
    async def coin(self, ctx: discord.ext.commands.context.Context):
        """
        Flips a coin with the result heads or tails
        """
        if ctx.message.guild:
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

        embed = discord.Embed(colour=int(self.bot.config["embed-colours"]["default"], 16), title=f"{self.bot.user.name} Stats", description="\uFEFF")

        embed.add_field(name="Total Servers", value=str(self.bot.total_server))
        embed.add_field(name="Total Users", value=str(self.bot.total_user))
        embed.add_field(name="Total Executed Commands", value=str(self.bot.total_executed_commands))
        embed.add_field(name="Total Lines of Code", value=self.bot.total_lines_code)
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
        if ctx.message.guild:
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
        embed = discord.Embed(
            title=f"I have deleted {amount} messages in this channel!",
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        )
        embed.set_footer(text="This message will delete itself after 15 seconds!")
        await ctx.send(embed=embed, delete_after=15)

    @commands.command(description="Info about a member")
    @commands.guild_only()
    async def member(self, ctx: commands.context.Context, user: discord.Member):
        roles = ""
        for role in user.roles:
            if role.name == "@everyone":
                continue
            roles += role.mention + "\n"

        if roles == "":
            roles = "@everyone"

        embed = discord.Embed(
            title=f"Info about {user.display_name}",
            colour=user.color,
            description=f"These are some information about {user.mention}"
        )
        embed.add_field(name="Tag", value=user.name + "#" + user.discriminator)
        embed.add_field(name="Nickname", value=user.display_name)
        embed.add_field(name="Status", value=user.status)
        embed.add_field(name="Roles", value=roles, inline=False)
        embed.add_field(name="Joined Server at", value=user.joined_at.strftime("%d, %b %Y at %H:%M"), inline=False)
        embed.add_field(name="Created Account at", value=user.created_at.strftime("%d, %b %Y at %H:%M"), inline=False)

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

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
