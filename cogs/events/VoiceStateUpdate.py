import discord
from discord.ext import commands


class VoiceStateUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        allowed_ids = []
        if member.id in allowed_ids:
            return

        if after.channel and after.channel.id == 536969317431115776:
            await member.send("You are not allowed to join this channel!")
            await member.move_to(None)



def setup(bot):
    bot.add_cog(VoiceStateUpdate(bot))
