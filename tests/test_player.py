from unittest import TestCase
import discord
from lib.player import Player


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
            point=1
        )

        expected = Player(
            self.discord_account,
            voting_rights=0,
            point=1
        )

        self.assertEqual(player.vote(), expected)

    def test_vote_no_voting_rights(self):
        player = Player(
            self.discord_account,
            voting_rights=0,
        )

        self.assertEqual(player.vote(), None)

    def test_add_point(self):
        player = Player(self.discord_account)

        expected = Player(self.discord_account, point=1)
        result = player.add_point(1)

        self.assertEqual(result, expected)

    def test_use_point(self):
        player = Player(self.discord_account, point=1)

        expected = Player(self.discord_account, point=0)
        result = player.use_point(1)

        self.assertEqual(result, expected)

    def test_use_point_when_not_enough(self):
        player = Player(self.discord_account)

        result = player.use_point(1)

        self.assertIsNone(result)

    def test_add_voting_rights(self):
        result = Player(self.discord_account).add_voting_rights(1)
        expected = Player(self.discord_account, voting_rights=1)

        self.assertEqual(result, expected)

    def test_update(self):
        result = Player(
            self.discord_account,
            votes_count=1,
            voting_rights=1,
            point=1
        ).update(point=0)

        expected = Player(
            self.discord_account,
            votes_count=1,
            voting_rights=1,
            point=0
        )

        self.assertEqual(result, expected)
