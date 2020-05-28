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

    def test_have_voting_rights(self):
        player = Player(
            self.discord_account,
            voting_rights=1,
        )

        self.assertTrue(player.has_voting_rights())

    def test_vote(self):
        player = Player(
            self.discord_account,
            voting_rights=1,
        )

        expected = Player(
            self.discord_account,
            voting_rights=0,
        )

        self.assertEqual(player.vote(), expected)

    def test_vote_no_voting_rights(self):
        player = Player(
            self.discord_account,
            voting_rights=0,
        )

        self.assertEqual(player.vote(), None)
