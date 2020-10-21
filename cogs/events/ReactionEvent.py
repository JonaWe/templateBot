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

        if reaction.emoji == self.bot.emoji["repeat"] and message.embeds:
            if message.embeds[0].title == "Flipping the coin!":
                self.bot.total_executed_commands += 1
                await embed_helper.send_coin_flip_embed(user, reaction.message.channel, self.bot)
            elif message.embeds[0].title == "Rolling the dice!":
                self.bot.total_executed_commands += 1
                await embed_helper.send_roll_dice_embed(user, reaction.message.channel, self.bot, 6)

        for k, v in self.bot.active_games.items():
            if reaction.message.id == v["message"].id:
                if not v["accepted"]:
                    if user.id == v["enemy"].id and reaction.emoji == "\U00002705":
                        game = v["game"]
                        embed = discord.Embed()
                        embed.title = f"Four Connect"
                        embed.description = f"{v['player'].mention} (:yellow_circle:) vs {user.mention} (:red_circle:)\n\uFEFF\n{game.to_embed_string()}"
                        embed.colour = int(self.bot.config["embed-colours"]["default"], 16)
                        if game.current_player == 1:
                            cp = v['player'].display_name
                        else:
                            cp = user.display_name
                        embed.add_field(name="Current Player", value=cp)
                        embed.set_footer(text="By clicking on the reaction u can place u chip.")

                        await message.clear_reactions()
                        await message.edit(embed=embed, content="")

                        v["accepted"] = True
                        v["started"] = int(round(time.time() * 1000))

                        # adds all the reaction to the message
                        await message.add_reaction("1\N{variation selector-16}\N{combining enclosing keycap}")
                        await message.add_reaction("2\N{variation selector-16}\N{combining enclosing keycap}")
                        await message.add_reaction("3\N{variation selector-16}\N{combining enclosing keycap}")
                        await message.add_reaction("4\N{variation selector-16}\N{combining enclosing keycap}")
                        await message.add_reaction("5\N{variation selector-16}\N{combining enclosing keycap}")
                        await message.add_reaction("6\N{variation selector-16}\N{combining enclosing keycap}")
                        await message.add_reaction("7\N{variation selector-16}\N{combining enclosing keycap}")


                    else:
                        await reaction.message.remove_reaction(reaction.emoji, user)
                else:
                    game = v["game"]
                    # reaction if from the player who is currently active
                    if game.current_player == 1 and user.id == v["player"].id \
                        or game.current_player == 2 and user.id == v["enemy"].id:
                        embed = v["embed"]
                        message = v["message"]
                        player = v['player']
                        enemy = v['enemy']

                        col = int(reaction.emoji[0]) - 1
                        if game.add_coin(game.current_player, col):
                            embed.description = f"{player.mention} (:yellow_circle:) vs {enemy.mention} (:red_circle:)\n\uFEFF\n{game.to_embed_string()}"

                            if game.current_player == 1:
                                cp = player.display_name
                            else:
                                cp = enemy.display_name
                            embed.clear_fields()
                            embed.add_field(name="Current Player", value=cp)

                            await message.edit(embed=embed)

                            # checking for an game end
                            winner = game.check_for_win()
                            if winner:
                                embed.clear_fields()
                                if winner == 1:
                                    embed.add_field(name="Winner", value=v["player"].display_name)
                                elif winner == 2:
                                    embed.add_field(name="Winner", value=v["enemy"].display_name)
                                else:
                                    embed.add_field(name="Draw", value="\uFEFF")
                                end = int(round(time.time() * 1000))
                                secs = int(round((end - int(v["started"])) / 1000))
                                embed.set_footer(text=f"This game took {secs} seconds to finish.")
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                self.bot.active_games.pop(str(player.id))
                        await reaction.message.remove_reaction(reaction.emoji, user)

                    # delete any other reactions
                    else:
                        await reaction.message.remove_reaction(reaction.emoji, user)



def setup(bot):
    bot.add_cog(ReactionEvent(bot))
