import discord
from discord.ext import commands

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
                        embed.description = f"{player.mention} vs {enemy.mention}\n\uFEFF\n{game.to_embed_string()}"

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
                            if winner == 1:
                                w = v["player"].display_name
                            else:
                                w = v["enemy"].display_name
                            embed.clear_fields()
                            embed.add_field(name="Winner", value=w)
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            self.bot.active_games.pop(str(player.id))
                    await reaction.message.remove_reaction(reaction.emoji, user)

                # delete any other reactions
                else:
                    await reaction.message.remove_reaction(reaction.emoji, user)



def setup(bot):
    bot.add_cog(ReactionEvent(bot))
