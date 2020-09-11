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
            print("---\nreaction from myself\n---")
            return

        message = reaction.message

        # reaction on user message
        if message.author != self.bot.user:
            print("---\nreaction to someone else\n---")
            return

        # author is blacklisted
        if user.id in self.bot.blacklisted_users:
            return

        # the reaction is not on embeds
        if not message.embeds:
            print("---\no embeds\n---")
            return
        elif reaction.emoji == self.bot.emoji["repeat"]:
            if message.embeds[0].title == "Flipping the coin!":
                await embed_helper.send_coin_flip_embed(user, reaction.message.channel, self.bot)
            elif message.embeds[0].title == "Rolling the dice!":
                await embed_helper.send_roll_dice_embed(user, reaction.message.channel, self.bot, 6)


def setup(bot):
    bot.add_cog(ReactionEvent(bot))
