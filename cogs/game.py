import discord
from discord.ext import commands
from lib.death_game import DeathGame
from lib.player import Player
from typing import Union


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = DeathGame()

    @commands.command()
    async def join(self, ctx):
        new_player = Player(ctx.author)
        self.game = self.game.join(new_player)

        await ctx.channel.send('参加完了')

    @commands.command()
    async def ranking(self, ctx):
        await ctx.channel.send('', embed=self.game.embed_votes_ranking())

    @commands.command()
    async def vote(
        self,
        ctx,
        voted_discord_account: Union[discord.Member, discord.User]
    ):
        voter = self.game.player_by_discord(ctx.author)
        voted_player = self.game.player_by_discord(voted_discord_account)

        if not voter.has_voting_rights():
            await ctx.channel.send('投票権がありません。')
            return

        if voted_player is None:
            await ctx.channel.send('投票先が見つかりませんでした。')
            return

        self.game = self.game.vote(voter, voted_player)

        await ctx.channel.send('投票しました。')


def setup(bot):
    bot.add_cog(Game(bot))
