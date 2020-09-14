import discord
from discord.ext import tasks, commands


class PresenceTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @tasks.loop(seconds=10.0)
    async def update_status(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                 name=f"{self.bot.total_server} servers "
                                                                      f"| {self.bot.DEFAULTPREFIX}help to start!"),
                                       status=discord.Status.online)

    @update_status.before_loop
    async def wait_function(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(PresenceTask(bot))
