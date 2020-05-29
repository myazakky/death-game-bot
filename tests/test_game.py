from unittest import TestCase
import discord
from cogs.death_game import DeathGame
from cogs.player import Player


class TestDeathDame(TestCase):
    def setUp(self):
        discord_account = discord.User(state=None, data={
            'username': None,
            'id': 0,
            'discriminator': None,
            'avatar': None
        })

        self.player = Player(discord_account)
        self.game = DeathGame()

    def test_equal(self):
        game1 = DeathGame([self.player])
        game2 = DeathGame([self.player])

        self.assertTrue(game1 == game2)

    def test_join(self):
        result = self.game.join(self.player)
        expected = DeathGame([self.player])

        self.assertEqual(result, expected)
