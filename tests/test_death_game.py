from unittest import TestCase
import discord
from lib.death_game import DeathGame
from lib.player import Player


class TestDeathDame(TestCase):
    def setUp(self):
        self.discord_account = self.new_discord_user(0)

        self.player = Player(self.discord_account)
        self.game = DeathGame()

    def new_discord_user(self, id):
        return discord.User(state=None, data={
            'username': None,
            'id': id,
            'discriminator': None,
            'avatar': None
        })

    def test_equal(self):
        game1 = DeathGame([self.player])
        game2 = DeathGame([self.player])

        self.assertTrue(game1 == game2)

    def test_join(self):
        result = self.game.join(self.player)
        expected = DeathGame([self.player])

        self.assertEqual(result, expected)

    def test_join_when_joined(self):
        result = self.game.join(self.player).join(self.player)
        expected = DeathGame([self.player])

        self.assertEqual(result, expected)

    def test_vote(self):
        voter = Player(self.new_discord_user(0), voting_rights=1)
        voted_player = Player(self.new_discord_user(1))
        steve = Player(self.new_discord_user(2))

        self.game = self.game.join(voter).join(voted_player).join(steve)

        result = self.game.vote(voter, voted_player)
        expected = DeathGame([voter.vote(), voted_player.voted(), steve])

        self.assertEqual(result, expected)

    def test_vote_no_rights(self):
        self.assertIsNone(self.game.vote(self.player, self.player))

    def test_player_by_discord(self):
        self.game = self.game.join(self.player)

        result = self.game.player_by_discord(self.discord_account)
        self.assertEqual(result, self.player)

    def test_votes_ranking(self):
        voter = Player(self.new_discord_user(0), voting_rights=1)
        voted_player = Player(self.new_discord_user(1))

        game = self.game.join(voter).join(voted_player)
        game = game.vote(voter, voted_player)

        ranking = game.votes_ranking()
        expected = [voted_player.voted(), voter.vote()]
        self.assertEqual(ranking, expected)

    def test_embed_votes_ranking(self):
        voter = Player(self.new_discord_user(0), voting_rights=1)
        voted_player = Player(self.new_discord_user(1))

        game = self.game.join(voter).join(voted_player)
        game = game.vote(voter, voted_player)

        expected = discord.Embed(title='得票数ランキング').add_field(
            name='1位', value='<@1>: 1票'
        )

        result = game.embed_votes_ranking()

        self.assertEqual(expected._fields, result._fields)
