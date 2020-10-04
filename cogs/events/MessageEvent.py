import discord
from discord.ext import commands


class MessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not await self.bot.check_message_reply(message, False):
            return

        prefix = self.bot.get_my_prefix(self.bot, message)

        # if the bot gets mentioned it replies
        if f"<@!{self.bot.user.id}>" in message.content:
            await message.channel.send(f"I If you need my help use `{prefix}help` to get a list of the available commands.")


def setup(bot):
    bot.add_cog(MessageEvent(bot))
