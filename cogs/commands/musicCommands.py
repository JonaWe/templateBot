import asyncio

import discord
from discord.ext import commands
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def form_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            data = data[0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.PCMVolumeTransformer(filename, **ffmpeg_options), data=data)

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

        await ctx.send(f"Connected to {channel.name} with the volume level {vc.source.volume}")

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

    @commands.command(description="Changes the volume of the bot")
    @commands.guild_only()
    async def volume(self, ctx: commands.context.Context, level: int=50):
        vc = ctx.voice_client

        if not vc:
            return await ctx.send("I am not connected to a voice channel right now.")

        if not  0 < level < 101:
            return await ctx.send("Select a volume level between 0 and 100.")

        if vc.source:
            # todo verify that the volume works
            vc.source.volume = level / 100

            await ctx.send(f"Changed the volume to {level}%")



def setup(bot):
    bot.add_cog(MusicCommands(bot))
