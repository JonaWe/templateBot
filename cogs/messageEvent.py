import discord
from discord.ext import commands

import json_helper


class MessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_message(self, message):
        # message from the bot
        if message.author == self.bot.user:
            return

        # dm message to the bot
        if isinstance(message.channel, discord.DMChannel):
            return

        # message is not in bot-commands channel
        # if message.channel.name != "bot-commands":
            # return

        # author is blacklisted
        if message.author.id in self.bot.blacklisted_users:
            return

        await self.bot.process_commands(message)

        prefix = json_helper.get_prefix(message.guild.id, self.bot)

        if message.content.startswith(f"{prefix}coinflip") \
                or message.content.startswith(f"{prefix}flip") \
                or message.content.startswith(f"{prefix}coin") \
                or message.content.startswith(f"{prefix}dice") \
                or message.content.startswith(f"{prefix}roll dice") \
                or message.content.startswith(f"{prefix}roll"):
            await message.delete()

        if f"<@!{self.bot.user.id}>" in message.content:
            await message.channel.send(f"I have heard my name.\nIf you need my help use "
                                       f"`{prefix}help`"
                                       f" to get a list of the available commands.")


def setup(bot):
    bot.add_cog(MessageEvent(bot))
