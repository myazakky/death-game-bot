from discord.ext import commands
from lib.death_game import DeathGame
from lib.player import Player


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = DeathGame()

    @commands.command()
    async def join(self, ctx):
        new_player = Player(ctx.author, voting_rights=1)
        self.game = self.game.join(new_player)

        await ctx.channel.send('参加完了')


def setup(bot):
    bot.add_cog(Game(bot))
