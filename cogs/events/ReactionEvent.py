import discord
from discord.ext import commands

import time
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
            return

        message = reaction.message

        # reaction on user message
        if message.author != self.bot.user:
            return

        # author is blacklisted
        if user.id in self.bot.blacklisted_users:
            return

        for listener in self.bot.reaction_listener:
            await listener(reaction)

        if reaction.emoji == self.bot.emoji["repeat"] and message.embeds:
            if message.embeds[0].title == "Flipping the coin!":
                self.bot.total_executed_commands += 1
                await embed_helper.send_coin_flip_embed(user, reaction.message.channel, self.bot)
            elif message.embeds[0].title == "Rolling the dice!":
                self.bot.total_executed_commands += 1
                await embed_helper.send_roll_dice_embed(user, reaction.message.channel, self.bot, 6)

        for k, v in self.bot.active_games.items():
            if reaction.message.id == v["message"].id:
                game_emojis = ["1\N{variation selector-16}\N{combining enclosing keycap}",
                                               "2\N{variation selector-16}\N{combining enclosing keycap}",
                                               "3\N{variation selector-16}\N{combining enclosing keycap}",
                                               "4\N{variation selector-16}\N{combining enclosing keycap}",
                                               "5\N{variation selector-16}\N{combining enclosing keycap}",
                                               "6\N{variation selector-16}\N{combining enclosing keycap}",
                                               "7\N{variation selector-16}\N{combining enclosing keycap}",
                                               "\U0000274c"]
                if not v["accepted"]:
                    if user.id == v["enemy"].id and reaction.emoji == "\U00002705":
                        self.bot.total_executed_commands += 1
                        game = v["game"]
                        embed = discord.Embed()
                        embed.title = "Connect Four"
                        embed.description = f":yellow_circle: ({v['player'].mention}) vs. :red_circle: ({user.mention})\n\uFEFF\n{game.to_embed_string()}"
                        if game.current_player == 1:
                            embed.colour = int("fdcb58", 16)
                            cp = v['player'].display_name
                        else:
                            embed.colour = int("dd2e44", 16)
                            cp = user.display_name
                        embed.add_field(name="Current Player", value=cp)
                        embed.set_footer(text="By clicking on the reaction u can place u chip.")

                        v["embed"] = embed

                        await message.clear_reactions()
                        await message.edit(embed=embed, content="")

                        v["accepted"] = True
                        v["started"] = int(round(time.time() * 1000))

                        # adds all the reaction to the message
                        for emoji in game_emojis:
                            await message.add_reaction(emoji)

                    elif user.id == v["enemy"].id and reaction.emoji == "\U0000274c":
                        self.bot.total_executed_commands += 1
                        embed = v["embed"]
                        embed.description = f"{v['enemy'].mention} has declined to play against {v['player'].mention}."
                        embed.set_footer(text="This game has been canceled!")
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        self.bot.active_games.pop(str(v["player"].id))
                    else:
                        await reaction.message.remove_reaction(reaction.emoji, user)

                elif reaction.emoji == "\U0000274c" and (user.id == v["player"].id or user.id == v["enemy"].id):
                    active_game = self.bot.active_games.get(str(v["player"].id))

                    game = active_game["game"]

                    embed = discord.Embed()
                    embed.title = "Connect Four"
                    embed.description = f":yellow_circle: ({active_game['player'].mention}) vs. :red_circle: ({active_game['enemy'].mention})\n\uFEFF\n{game.to_embed_string()}"
                    embed.colour = int(self.bot.config["embed-colours"]["default"], 16)

                    if user.id == active_game["player"].id:
                        embed.colour = int("dd2e44", 16)
                        embed.add_field(name="Winner _(opponent quit)_", value=active_game["enemy"].display_name)
                    else: # if user.id == active_game["enemy"].id:
                        embed.colour = int("fdcb58", 16)
                        embed.add_field(name="Winner _(opponent quit)_", value=active_game["player"].display_name)

                    end = int(round(time.time() * 1000))
                    secs = int(round((end - int(active_game["started"])) / 1000))
                    embed.set_footer(text=f"This game took {secs} seconds to finish.")
                    await active_game["message"].edit(embed=embed)
                    await active_game["message"].clear_reactions()
                    self.bot.active_games.pop(str(active_game["player"].id))

                elif reaction.emoji in game_emojis:
                    game = v["game"]
                    # reaction if from the player who is currently active
                    if game.current_player == 1 and user.id == v["player"].id \
                        or game.current_player == 2 and user.id == v["enemy"].id:
                        self.bot.total_executed_commands += 1
                        embed = v["embed"]
                        message = v["message"]
                        player = v['player']
                        enemy = v['enemy']

                        col = int(reaction.emoji[0]) - 1
                        if game.add_coin(game.current_player, col):
                            embed.description = f":yellow_circle: ({player.mention}) vs.  :red_circle: ({enemy.mention})\n\uFEFF\n{game.to_embed_string()}"

                            if game.current_player == 1:
                                cp = player.display_name
                                embed.colour = int("fdcb58", 16)
                            else:
                                embed.colour = int("dd2e44", 16)
                                cp = enemy.display_name
                            embed.clear_fields()
                            embed.add_field(name="Current Player", value=cp)



                            # checking for an game end
                            winner = game.check_for_win()
                            if winner:
                                embed.clear_fields()
                                if winner == 1:
                                    embed.colour = int("fdcb58", 16)
                                    embed.add_field(name="Winner", value=v["player"].display_name)
                                elif winner == 2:
                                    embed.colour = int("dd2e44", 16)
                                    embed.add_field(name="Winner", value=v["enemy"].display_name)
                                else:
                                    embed.add_field(name="Draw", value="\uFEFF")
                                end = int(round(time.time() * 1000))
                                secs = int(round((end - int(v["started"])) / 1000))
                                embed.set_footer(text=f"This game took {secs} seconds to finish.")
                                await message.clear_reactions()
                                self.bot.active_games.pop(str(player.id))
                            await message.edit(embed=embed)
                        await reaction.message.remove_reaction(reaction.emoji, user)
                    # delete any other reactions
                    else:
                        await reaction.message.remove_reaction(reaction.emoji, user)

                # delete any other reactions
                else:
                    await reaction.message.remove_reaction(reaction.emoji, user)



def setup(bot):
    bot.add_cog(ReactionEvent(bot))
