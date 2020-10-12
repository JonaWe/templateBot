import discord
from discord.ext import commands
from better_profanity import profanity


class MessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.config["profanity-check"]:
            if profanity.contains_profanity(message.content) and isinstance(message.channel, discord.TextChannel):
                await message.delete()

                # todo check if the content is longer than the max chars for the description
                censored_content = profanity.censor(message.content, '\\*')

                embed = discord.Embed(
                    title=f"I have deleted a message from {message.author.display_name} because it contains bad words! ",
                    description=f"Content of the message:\n||{censored_content}||\n\uFEFF",
                    colour=int(self.bot.config["embed-colours"]["default"], 16)
                )

                embed.set_footer(text="This message will delete itself after 15 seconds!")
                await message.channel.send(embed=embed, delete_after=15)

        if not await self.bot.check_message_reply(message, False):
            return

        prefix = self.bot.get_my_prefix(self.bot, message)

        # if the bot gets mentioned it replies
        if f"<@!{self.bot.user.id}>" in message.content:
            await message.channel.send(embed=discord.Embed(
                title=f"I If you need my help use `{prefix}help` to get a list of the available commands.",
                colour=int(self.bot.config["embed-colours"]["default"], 16)
            ))


def setup(bot):
    bot.add_cog(MessageEvent(bot))
