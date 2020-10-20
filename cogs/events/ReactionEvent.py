import discord
from discord.ext import commands

import embed_helper


class ReactionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        # reaction from the bot itself
        if user == self.bot.user:
            return

        message = reaction.message

        # reaction on user message
        if message.author != self.bot.user:
            return

        # author is blacklisted
        if user.id in self.bot.blacklisted_users:
            return

        if reaction.emoji == self.bot.emoji["repeat"] and message.embeds:
            if message.embeds[0].title == "Flipping the coin!":
                self.bot.total_executed_commands += 1
                await embed_helper.send_coin_flip_embed(user, reaction.message.channel, self.bot)
            elif message.embeds[0].title == "Rolling the dice!":
                self.bot.total_executed_commands += 1
                await embed_helper.send_roll_dice_embed(user, reaction.message.channel, self.bot, 6)

        for k, v in self.bot.active_games.items():
            if reaction.message.id == v["message"].id:
                embed = v["embed"]
                message = v["message"]
                await message.channel.send("yeeeeeee")


def setup(bot):
    bot.add_cog(ReactionEvent(bot))
