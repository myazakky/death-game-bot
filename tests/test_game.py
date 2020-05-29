from unittest import TestCase
import discord
from lib.death_game import DeathGame
from lib.player import Player


class TestDeathDame(TestCase):
    def setUp(self):
        self.discord_account = discord.User(state=None, data={
            'username': None,
            'id': 0,
            'discriminator': None,
            'avatar': None
        })

        self.player = Player(self.discord_account)
        self.game = DeathGame()

    def test_equal(self):
        game1 = DeathGame([self.player])
        game2 = DeathGame([self.player])

        self.assertTrue(game1 == game2)

    def test_join(self):
        result = self.game.join(self.player)
        expected = DeathGame([self.player])

        self.assertEqual(result, expected)

    def test_vote(self):
        voter = Player(self.discord_account, voting_rights=1)
        voted_player = Player(self.discord_account)

        self.game.join(voter)
        self.game.join(voted_player)

        result = self.game.vote(voter, voted_player)
        expected = DeathGame([voter.vote(), voted_player.voted()])

        self.assertEqual(result, expected)
