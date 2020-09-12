import discord
from discord.ext import commands
import random
from platform import python_version


async def send_coin_flip_embed(user: discord.User, channel, bot: commands.Bot):
    embed = discord.Embed(colour=bot.embed_colour)

    embed.set_author(name=f"{user.name} requested a coinflip", icon_url=user.avatar_url)
    embed.title = f"Flipping the coin!"
    embed.description = f"\uFEFF\n**{random.choice(['HEADS', 'TAILS'])}**\n\uFEFF"
    embed.add_field(name=f"0", value=f"total flips {user.mention}")
    embed.set_footer(text="You can flip again by clicking the repeat reaction", icon_url=bot.user.avatar_url)

    message = await channel.send(embed=embed)
    await message.add_reaction(bot.emoji["repeat"])


async def send_roll_dice_embed(user: discord.User, channel, bot: commands.Bot, max_value: int):
    embed = discord.Embed(colour=bot.embed_colour)

    embed.set_author(name=f"{user.name} requested a diceroll", icon_url=user.avatar_url)
    embed.title = f"Rolling the dice!"
    embed.description = f"\uFEFF\n**{random.randint(1, max_value)}**\n\uFEFF"
    embed.add_field(name=f"0", value=f"total rolls {user.mention}")
    embed.set_footer(text="You can roll again by clicking the repeat reaction", icon_url=bot.user.avatar_url)

    message = await channel.send(embed=embed)
    await message.add_reaction(bot.emoji["repeat"])


async def send_stats_embed(ctx, bot: commands.Bot):
    embed = discord.Embed(colour=bot.embed_colour, title=f"{bot.user.name} Stats", description="\uFEFF")

    embed.timestamp = ctx.message.created_at
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    embed.add_field(name="Total Servers", value=str(bot.total_server))
    embed.add_field(name="Total Users", value=str(bot.total_user))
    embed.add_field(name="Bot Version", value=str(bot.version))
    embed.add_field(name="Running on", value=f"Python {python_version()}")
    embed.add_field(name="Discord.py Version", value=f"{discord.__version__}")
    embed.add_field(name="Developer", value=bot.author_mention)

    embed.set_footer(text=f"{bot.user.name}")

    await ctx.send(embed=embed)
