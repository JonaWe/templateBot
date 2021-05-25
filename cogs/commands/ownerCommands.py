import asyncio
import os
import string
import unicodedata
from json import loads

import discord
import youtube_dl
from discord.ext import commands

import customErrors.errors
import json_helper

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:char_limit]


class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog has been loaded\n---------")

    # region YouTube-To-mp3 Command

    @commands.command(name="yt2mp3",
                      aliases=["yt"],
                      description="Downloads the audio of a YouTube video")
    @commands.is_owner()
    async def youtube_to_mp3(self, ctx: commands.context.Context, *, video_url: str):
        with ctx.typing():
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=video_url, download=False
            )

            filename = clean_filename(video_info['title'])

            SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/yt_downloads'

            options = {
                'format': 'bestaudio/best',
                "keepvideo": False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': SAVE_PATH + f"/{filename}.%(ext)s",

            }

            with youtube_dl.YoutubeDL(options) as ytdl:
                ytdl.download([video_info["webpage_url"]])

            await ctx.send(file=discord.File(f"yt_downloads/{filename}.mp3"))

    # endregion

    # region Devmode Commands

    @commands.group(description="Turning the devmode on an off",
                    aliases=["dm", "d"])
    @commands.is_owner()
    @commands.bot_has_guild_permissions(send_messages=True)
    async def devmode(self, ctx: discord.ext.commands.context.Context):
        """
        Interaction with the devmode of this bot.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired()

    @devmode.command(description="Turns devmode on")
    @commands.is_owner()
    async def on(self, ctx: discord.ext.commands.context.Context):
        """
        Turns the devmode of this bot on so that other users cannot interact with it.
        """
        self.bot.config["devmode"] = True
        json_helper.write_json("config", self.bot.config)

        await ctx.send(embed=discord.Embed(
            description="```diff\n+ Devmode has been turned on```",
            colour=int(self.bot.config["embed-colours"]["confirm"], 16)
        ))

    @devmode.command(description="Turns devmode off")
    @commands.is_owner()
    async def off(self, ctx: discord.ext.commands.context.Context):
        """
        Turns the devmode of this bot off so that other users can interact with it.
        """
        self.bot.config["devmode"] = False
        json_helper.write_json("config", self.bot.config)

        await ctx.send(embed=discord.Embed(
            description="```diff\n- Devmode has been turned off```",
            colour=int(self.bot.config["embed-colours"]["warning"], 16)
        ))

    @devmode.command(description="Returns the devmode state",
                     aliases=["state", "s"])
    @commands.is_owner()
    async def status(self, ctx: discord.ext.commands.context.Context):
        """
        This command returns the devmode state the bot is currently in.
        """
        embed = discord.Embed()
        if self.bot.config["devmode"]:
            embed.colour = int(self.bot.config["embed-colours"]["confirm"], 16)
            embed.description = "```diff\n+ Devmode is currently turned on```"
        else:
            embed.colour = int(self.bot.config["embed-colours"]["warning"], 16)
            embed.description = "```diff\n- Devmode is currently turned off```"
        await ctx.send(embed=embed)

    # endregion

    # region Blacklist Commands

    @commands.group(description="Manage the blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx: discord.ext.commands.context.Context):
        """
        Interaction with the blacklist of this bot.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired

    @blacklist.command(description="Blacklists users form the bot",
                       aliases=["a"])
    async def add(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        """
        Blacklists users from the bot. The blacklisted users cannot use any commands from this bot.
        """
        if user.id in self.bot.blacklisted_users:
            await ctx.send(embed=discord.Embed(
                title=f"`{user.display_name}` was already in the blacklist.",
                colour=int(self.bot.config["embed-colours"]["error"], 16)
            ))
            return
        self.bot.blacklisted_users.append(user.id)
        async with asyncio.Lock():
            data = json_helper.read_json("blacklist")
            data["commandBlacklistedUsers"].append(user.id)
            json_helper.write_json("blacklist", data)

        await ctx.send(embed=discord.Embed(
            title=f"`{user.display_name}` has been added to the blacklist.",
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        ))

    @blacklist.command(description="Removes users from the blacklist for this bot",
                       aliases=["r"])
    async def remove(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        """
        Removes users from blacklist for bot commands.
        """
        if user.id not in self.bot.blacklisted_users:
            await ctx.send(embed=discord.Embed(
                title=f"`{user.display_name}` was not found in the blacklist and therefore could not be removed from it.",
                colour=int(self.bot.config["embed-colours"]["error"], 16)
            ))
            await ctx.send(
                f"{user.display_name} was not found in the blacklist and therefore could not be removed from it.")
            return

        self.bot.blacklisted_users.remove(user.id)
        async with asyncio.Lock():
            data = json_helper.read_json("blacklist")
            data["commandBlacklistedUsers"].remove(user.id)
            json_helper.write_json("blacklist", data)

        await ctx.send(embed=discord.Embed(
            title=f"`{user.display_name}` has been removed from the blacklist.",
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        ))

    # endregion

    # region Config Commands

    @commands.group(description="Manage the config",
                    aliases=["c"])
    @commands.is_owner()
    async def config(self, ctx: commands.context.Context):
        """
        Interaction with the config of this bot.
        """
        if ctx.invoked_subcommand is None:
            raise customErrors.errors.SubCommandRequired()

    @config.command(description="Updating values in the config",
                    aliases=['u'])
    async def update(self, ctx: discord.ext.commands.context.Context, variable: str, *value):
        """
        Updating a specific value in the config.
        """
        # turn value argument into string
        value = " ".join(value)

        # if the variable is not in the config an error message will be send
        if variable not in self.bot.config:
            await ctx.send(embed=discord.Embed(
                title=f"The variable `{variable}` does not exits in the config of the bot! Therefore it was not updated.",
                colour=int(self.bot.config["embed-colours"]["default"], 16)
            ))
            return

        # if the variable is a string it will be converted to a string else the json converter will handle it
        if isinstance(self.bot.config, str):
            value = str(value)
        else:
            try:
                value = loads(value)
            except:
                raise commands.BadArgument

        # updating the config
        self.bot.config[variable] = value
        json_helper.write_json("config", self.bot.config)
        await ctx.send(embed=discord.Embed(
            title=f"Successfully updated `{variable}` to `{value}`.",
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        ))

    @config.command(name="reload",
                    description="Reloads the config",
                    aliases=['r'])
    @commands.is_owner()
    async def _reload(self, ctx: discord.ext.commands.context.Context):
        """
        Reloads the config file into the bot instance.
        """
        self.bot.config = json_helper.read_json("config")
        await ctx.send(embed=discord.Embed(
            title="Successfully reloaded the config!",
            colour=int(self.bot.config["embed-colours"]["default"], 16)
        ))

    # endregion

    # region HexToInt Command

    @commands.command(description="Converts hex to integer",
                      aliases=['hti'])
    @commands.is_owner()
    async def hextoint(self, ctx: commands.context.Context, hexnumber: str):
        """
        Converts a hexadecimal number into an integer.
        """
        try:
            num = int(hexnumber, 16)
            await ctx.send(f"Converted the hex number `{str(hexnumber)}` to the integer `{str(num)}`.")
        except:
            raise commands.BadArgument()

    # endregion

    # region Reload Command

    @commands.is_owner()
    @commands.command(description="Reloads COGs",
                      aliases=["r"])
    async def reload(self, ctx: commands.context.Context, cog=None):
        """
        Reloads either all or a specific cog from this bot.
        """

        # reloads a specific cog
        if cog:
            if "Command" in cog:
                path = "commands"
            elif "Event" in cog:
                path = "events"
            elif "Task" in cog:
                path = "tasks"
            else:
                raise customErrors.errors.CogDoesNotExist()

            print(f"./cogs/{path}/{cog}.py")
            if not os.path.exists(f"{json_helper.get_cwd()}/cogs/{path}/{cog}.py"):
                raise customErrors.errors.CogDoesNotExist()

            try:
                print(path, cog)
                print(f"cogs.{path}.{cog}")
                self.bot.unload_extension(f"cogs.{path}.{cog}")
                self.bot.load_extension(f"cogs.{path}.{cog}")
                embed = discord.Embed(title=f"Successfully reloaded **{cog}**",
                                      colour=int(self.bot.config["embed-colours"]["default"], 16))
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title=f"Failed to reload **{cog}**",
                                      colour=int(self.bot.config["embed-colours"]["default"], 16))
                await ctx.send(embed=embed)


        # reloads all cogs
        else:
            embed = discord.Embed(
                title="Reloading all cogs", colour=int(self.bot.config["embed-colours"]["default"], 16))
            cog_types = ["events", "commands", "tasks"]
            successful_cogs = ""
            failed_cogs = ""
            for cog_type in cog_types:
                for file in os.listdir(f"{self.bot.cwd}/cogs/{cog_type}"):
                    if file.endswith(".py"):
                        try:
                            self.bot.unload_extension(f"cogs.{cog_type}.{file[:-3]}")
                            self.bot.load_extension(f"cogs.{cog_type}.{file[:-3]}")
                            successful_cogs += f"`{file}`\n"
                        except:
                            failed_cogs += f"`{file}`\n"

            if successful_cogs != "":
                embed.add_field(name="Successfully reloaded:", value=successful_cogs, inline=False)

            if failed_cogs != "":
                embed.add_field(name="Failed to reload:", value=failed_cogs, inline=False)

            await ctx.send(embed=embed)

    # endregion


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
