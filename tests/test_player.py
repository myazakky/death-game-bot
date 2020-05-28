from unittest import TestCase
import discord
from cogs.player import Player


class TestPlayer(TestCase):
    def setUp(self):
        self.discord_account = discord.User(state=None, data={
            'username': None,
            'id': 0,
            'discriminator': None,
            'avatar': None
        })

    def test_equal(self):
        p1 = Player(self.discord_account)
        p2 = Player(self.discord_account)

        self.assertTrue(p1 == p2)

    def test_voted(self):
        player = Player(
            self.discord_account,
            votes_count=0,
        )

        expected = Player(
            self.discord_account,
            votes_count=1,
        )

        self.assertEqual(player.voted(), expected)
