import discord
from discord.ext import commands


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")


    @commands.command(name="connect",
                      description="Connects the bot to a voice channel",
                      aliases=["join"])
    @commands.guild_only()
    async def connect_(self, ctx: commands.context.Context, *, channel: discord.VoiceChannel=None):
        if not channel:
            if ctx.author.voice.channel:
                channel = ctx.author.voice.channel
            else:
                await ctx.send("You are not connected to a voice channel!")

        vc = ctx.voice_client

        # connected to a voice channel
        if vc:
            if vc.channel.id == channel.id:
                await ctx.send("I am already connected to your voice channel")
            else:
                await vc.move_to(channel)

        # not connected to a voice channel
        else:
            await channel.connect()

        await ctx.send(f"Connected to {channel.name}")

    @commands.command(name="disconnect",
                      aliases=["leave", "stop"],
                      description="Disconnects the bot for the voice channel")
    @commands.guild_only()
    async def disconnect_(self, ctx: commands.context.Context):
        vc = ctx.voice_client

        if vc:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I am currently not connected to any channel")



def setup(bot):
    bot.add_cog(MusicCommands(bot))
