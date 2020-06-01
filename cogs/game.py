import discord
from discord.ext import commands, tasks
import datetime
import asyncio
from lib.death_game import DeathGame
from lib.player import Player
from typing import Union


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = DeathGame()
        self.bot.loop.create_task(self.setup())

    async def setup(self):
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(year=now.year, month=now.month, day=now.day + 1)

        await asyncio.sleep(tomorrow.timestamp() - now.timestamp())
        self.tomorrow.start()

    @commands.command()
    async def join(self, ctx):
        new_player = Player(ctx.author)
        self.game = self.game.join(new_player)

        await ctx.channel.send('参加完了')

    @commands.command()
    async def ranking(self, ctx):
        await ctx.channel.send('', embed=self.game.embed_votes_ranking())

    @commands.command()
    async def real(self, ctx):
        buyer = self.game.player_by_discord(ctx.author)
        if buyer.point < 2:
            await ctx.channel.send('ポイントが不足しています。')
            return

        self.game = self.game.update_player(buyer, buyer.use_point(2))
        embed_ranking = self.game.embed_real_votes_ranking()
        await ctx.channel.send('', embed=embed_ranking)

    @commands.command()
    async def guess(self, ctx, target: Union[discord.Member, discord.User]):
        guesser = self.game.player_by_discord(ctx.author)
        target = self.game.player_by_discord(target)

        if guesser.guess(target) is None:
            await ctx.channel.send('予想は1日１回までです。')
            return

        self.game = self.game.guess(guesser, target)
        await ctx.channel.send('予想しました。')

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

    @commands.command()
    async def fake(
        self,
        ctx,
        voted_discord_account: Union[discord.Member, discord.User]
    ):
        voter = self.game.player_by_discord(ctx.author)
        voted_player = self.game.player_by_discord(voted_discord_account)

        if not voter.has_fake_voting_rights():
            await ctx.channel.send('嘘投票権がありません。')
            return

        if voted_player is None:
            await ctx.channel.send('嘘投票先が見つかりませんでした。')
            return

        self.game = self.game.fake_vote(voter, voted_player)

        await ctx.channel.send('嘘投票しました。')

    @commands.command()
    async def more(self, ctx):
        buyer = self.game.player_by_discord(ctx.author)

        if self.game.buy_voting_rights(buyer) is None:
            await ctx.channel.send('ポイントが不足しています。')
            return

        self.game = self.game.buy_voting_rights(buyer)

        await ctx.channel.send('投票権を付与しました。')

    @commands.command()
    async def more_fake(self, ctx):
        buyer = self.game.player_by_discord(ctx.author)

        if self.game.buy_fake_voting_rights(buyer) is None:
            await ctx.channel.send('ポイントが不足しています。')
            return

        self.game = self.game.buy_fake_voting_rights(buyer)

        await ctx.channel.send('嘘投票権を付与しました。')

    @commands.command()
    async def point(self, ctx):
        player = self.game.player_by_discord(ctx.author)
        await ctx.channel.send(f'{player.point}ポイント')

    @commands.command()
    async def status(self, ctx):
        player = self.game.player_by_discord(ctx.author)
        if player.guessed is None:
            target = None
        else:
            target = player.guessed.discord_account.name


        sent_message = f'''
```
得票数: {player.votes_count}
嘘得票数: {player.fake_votes_count}
投票権: {player.voting_rights}
嘘投票権: {player.fake_voting_rights}
ポイント: {player.point}
予想: {target}
```
        '''

        await ctx.channel.send(sent_message)

    @tasks.loop(hours=24)
    async def tomorrow(self):
        self.game = self.game.go_to_tomorrow()


def setup(bot):
    bot.add_cog(Game(bot))
