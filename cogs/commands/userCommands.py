import asyncio
import time
import discord
import random
from discord.ext import commands
from platform import python_version
from games import four_connect
import customErrors


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    #region Four-Connect Game

    @commands.group(description="Managing a four connect game",
                      aliases=["fc"])
    @commands.guild_only()
    async def fourconnent(self, ctx):
        """
        With this command you can manage your four connect game.
        """
        if ctx.invoked_subcommand is None:
            await self.start(ctx)

    #region End

    @fourconnent.command(description="Ends a four connect game",
                         aliases=["e", "stop", "exit", "quit", "leave"])
    async def end(self, ctx: commands.context.Context):
        """
        This commands ends your current four connect game.
        """
        if f"{ctx.author.id}" in self.bot.active_games:

            active_game = self.bot.active_games.get(str(ctx.author.id))

            game = active_game["game"]

            embed = discord.Embed()
            embed.title = "Connect Four"
            embed.description = f"{active_game['player'].mention} (:yellow_circle:) vs {active_game['enemy'].mention} (:red_circle:)\n\uFEFF\n{game.to_embed_string()}"
            embed.colour = int(self.bot.config["embed-colours"]["default"], 16)

            if ctx.author.id == active_game["player"].id:
                embed.add_field(name="Winner _(opponent quit)_", value=active_game["enemy"].display_name)
            else:
                embed.add_field(name="Winner _(opponent quit)_", value=active_game["player"].display_name)

            end = int(round(time.time() * 1000))
            secs = int(round((end - int(active_game["started"])) / 1000))
            embed.set_footer(text=f"This game took {secs} seconds to finish.")
            await active_game["message"].edit(embed=embed)
            await active_game["message"].clear_reactions()
            self.bot.active_games.pop(str(active_game["player"].id))
        else:
            await ctx.send(embed=discord.Embed(
                colour=int(self.bot.config["embed-colours"]["warning"], 16),
                title="You don't have an active connect four game running!"
            ))

    #endregion

    #region Start

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
        embed.title = "Connect Four"
        embed.description = f"{ctx.author.mention} has challenged {user.mention} to play four connect."
        embed.set_footer(text="Reply with the checkmark to accept the game invite.")
        embed.colour = int(self.bot.config["embed-colours"]["default"], 16)

        message = await ctx.send(embed=embed, content=str(user.mention))

        await message.add_reaction("\U00002705")
        await message.add_reaction("\U0000274c")

        self.bot.active_games[f"{ctx.author.id}"] = {
            "accepted": False,
            "started": 0,
            "player": ctx.author,
            "enemy": user,
            "game": game,
            "embed": embed,
            "message": message
        }

    #endregion

    #endregion

    #region Coin Command

    @commands.command(aliases=['flip', 'coinflip', 'cf'],
                      ignore_extra=False,
                      description="Flips a coin")
    async def coin(self, ctx: commands.context.Context):
        """
        Flips a coin with the result heads or tails
        """
        message: discord.Message = await ctx.channel.send(embed=self.coin_embed(self.bot, ctx))

        async def reroll(reaction: discord.Reaction, user: discord.User):
            await reaction.remove(user)
            if user != ctx.message.author:
                return

            await message.edit(embed=self.coin_embed(self.bot, ctx))

        await self.bot.add_reaction_listener(reroll, message, '🔁', add_reaction=True)

    @staticmethod
    def coin_embed(bot, ctx):
        result = random.choice(['HEADS', 'TAILS'])
        embed = discord.Embed(
            colour=int(bot.config["embed-colours"]["default"], 16),
            title=f"Coin has been flipped!",
            description=f"\uFEFF\n**{result}**\n\uFEFF"
        )

        embed.set_author(name=f"{ctx.author.name} requested a coinflip", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="You can flip again by clicking the repeat reaction", icon_url=bot.user.avatar_url)
        return embed

    #endregion

    #region Stats Command

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

    #endregion

    #region Dice Command

    @commands.command(aliases=['roll dice', 'roll', 'rtd'],
                      description="Rolls a dice")
    async def dice(self, ctx: discord.ext.commands.context.Context, *number):
        """
        Rolls a dice from 1-6. If you add a number after the command you can set the dice range.
        """
        max_value= 0
        if number:
            if number[0].isnumeric():
                max_value = int(number[0])
            else:
                raise discord.ext.commands.BadArgument("Number expected")
        else:
            max_value = 6

        message: discord.Message = await ctx.channel.send(embed=self.dice_embed(self.bot, ctx, max_value=max_value))

        async def reroll(reaction: discord.Reaction, user: discord.User):
            await reaction.remove(user)
            if user != ctx.message.author:
                return

            await message.edit(embed=self.dice_embed(self.bot, ctx, max_value=max_value))

        await self.bot.add_reaction_listener(reroll, message, '🔁', add_reaction=True)


    @staticmethod
    def dice_embed(bot, ctx, max_value=6):
        embed = discord.Embed(colour=int(bot.config["embed-colours"]["default"], 16))

        embed.set_author(name=f"{ctx.author.name} requested a diceroll", icon_url=ctx.author.avatar_url)
        embed.title = f"Rolling the dice!"
        embed.description = f"\uFEFF\n**{random.randint(1, max_value)}**\n\uFEFF"
        if max_value != 6:
            embed.add_field(name="Custom max value", value=str(max_value))
        embed.set_footer(text="You can roll again by clicking the repeat reaction", icon_url=bot.user.avatar_url)

        return embed

    #endregion

    #region Wipe Command

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

    #endregion

    #region Member Command

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

    #endregion

    #region Invite Command

    @commands.command(description="Sends bot invite link",
                      ignore_extra=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: discord.ext.commands.context.Context):
        """
        Sends an invite link for this bot, so you can add it to you own server.
        """
        await ctx.send(self.bot.config["bot-invite-link"])

    #endregion C

    #region Multi-Quote Command

    @commands.command(name="multiquote",
                      aliases=["mq"],
                      description="Quotes a Conversaton user.")
    async def multi_quote(self, ctx : commands.context.Context, *, quote):
        splitted = quote.split('\"')

        print(splitted)

        #if splitted[:1] != "":
        #    print("Error 1")
        splitted = splitted[1:]
        quotes = []

        print(splitted)

        while len(splitted) > 1:
            quote = splitted[:1]
            author = splitted[:2]
            quotes.append((author, quote))
            splitted = splitted[2:]

        for a, q in quotes:
            print(a, q)

    #endregion

    #region Quote Command

    @commands.command(name="quote",
                      aliases=["q"],
                      description="Quotes a user.")
    async def quote(self, ctx: commands.context.Context, user:discord.Member, *, quote):
        """
        This command can be used to quote users. This command only works if a quote channel has been setup. You can setup a quote channel using the command: update quote_channel
        """
        quote_channels = self.bot.channel_ids["quotes"]
        guild_id = ctx.guild.id

        embed =discord.Embed()

        # quote channel is not setup
        if not str(guild_id) in quote_channels:
            embed.title = "The quote channel has not been set up yet."
            embed.colour = int(self.bot.config["embed-colours"]["warning"], 16)
            embed.description = f"Use `{ctx.prefix}update quote_channel <channel>` to setup the quote channel for this server!"
            await ctx.channel.send(embed=embed)
            return

        quote_channel = self.bot.get_channel(quote_channels[str(guild_id)])

        # check if the quote channel is a valid channel
        if not quote_channel:
            embed.title = "The quote channel is invalid!"
            embed.colour = int(self.bot.config["embed-colours"]["error"], 16)
            embed.description = f"Use `{ctx.prefix}update quote_channel <channel>` to setup the quote channel for this server!"
            await ctx.channel.send(embed=embed)
            return

        # creates the embed object for the quote
        embed.colour = user.colour
        embed.title = "\uFEFF"
        embed.set_author(name=f"{ctx.author.name} quoted {user.display_name}", icon_url=ctx.author.avatar_url)
        embed.title = f"\uFEFF\n\"{quote}\"\n\uFEFF\n"
        embed.set_footer(text=f"{user.display_name}", icon_url=user.avatar_url)
        embed.timestamp = ctx.message.created_at

        await quote_channel.send(embed=embed)

    #endregion

    #region Shuffle Command

    @commands.command(name="shuffle",
                      aliases=["random-teams"],
                      description="Creates random teams!")
    @commands.guild_only()
    @commands.cooldown(1, 30, type=commands.BucketType.guild)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.has_guild_permissions(move_members=True)
    async def shuffle(self, ctx: commands.context.Context, channel_1: discord.VoiceChannel, channel_2: discord.VoiceChannel):
        if not ctx.author.voice:
            embed = discord.Embed(
                title="You are not connected to a voice channel!",
                description="In order to execute this command you need to be connected to a voice channel.",
                colour=int(self.bot.config["embed-colours"]["warning"], 16)
            )
            await ctx.send(embed=embed)
            return

        members_in_source = ctx.author.voice.channel.members

        if len(members_in_source) < 2:
            embed = discord.Embed(
                title="There is a minimum of two users required to create a teams!",
                description=f"Only the users in `{ctx.author.voice.channel.name}` will be counted in.",
                colour=int(self.bot.config["embed-colours"]["warning"], 16)
            )
            await ctx.send(embed=embed)
            return
        async def shuffle_teams():
            team1, team2 = self.split_list_into_two_lists(members_in_source)

            await self.move_users_into_channel(team1, channel_1)
            await self.move_users_into_channel(team2, channel_2)

            team1_mentions = self.mention_all_users(team1)
            team2_mentions = self.mention_all_users(team2)

            embed = discord.Embed(
                title="Random teams have been created!",
                description=f"I have collected **{len(members_in_source)}** users from `{ctx.author.voice.channel.name}` and put them into random teams!",
                colour=int(self.bot.config["embed-colours"]["default"], 16)
            )
            embed.add_field(name=f"Team 1 `({channel_1.name})`", value=team1_mentions)
            embed.add_field(name=f"Team 2 `({channel_2.name})`", value=team2_mentions)

            return embed

        embed = await shuffle_teams()
        message = await ctx.send(embed=embed)

        async def reroll_teams(reaction: discord.Reaction, user: discord.User):
            if user != ctx.message.author:
                await reaction.remove(user)
                return

            embed = await shuffle_teams()
            await message.edit(embed=embed)
            await reaction.remove(user)

        await self.bot.add_reaction_listener(reroll_teams, message, '🔁', add_reaction=True)

    @staticmethod
    def split_list_into_two_lists(l: list):
        random.shuffle(l)
        team1 = l[len(l) // 2:]
        team2 = l[:len(l) // 2]
        return team1, team2

    @staticmethod
    async def move_users_into_channel(users: list, channel: discord.VoiceChannel):
        await asyncio.gather(*[user.move_to(channel) for user in users])

    @staticmethod
    def mention_all_users(users: list):
        output = ""
        for user in users:
            output += user.mention + '\n'
        return output

    #endregion

    #region Test Command
    @commands.command(name='test',
                      ignore_extra=False,
                      aliases=['t'],
                      hidden=True)
    @commands.cooldown(1, 75, commands.BucketType.user)
    @commands.bot_has_guild_permissions(administrator=True, kick_members=True, ban_members=True, manage_roles=True)
    async def test(self, ctx: discord.ext.commands.context.Context):
        message = await ctx.send("yoooo")

        async def test(reaction: discord.Reaction):
            await message.edit(content='this works fine!')
            print(reaction.emoji)

        await self.bot.add_reaction_listener(test, message, '🙃', add_reaction=True)

    #endregion

def setup(bot):
    bot.add_cog(UserCommands(bot))
