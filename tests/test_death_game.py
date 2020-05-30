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
        expected = DeathGame(
            [Player(self.discord_account, voting_rights=1, point=10)]
        )

        self.assertEqual(result, expected)

    def test_join_when_joined(self):
        result = self.game.join(self.player).join(self.player)
        expected = DeathGame([self.player.add_voting_rights(1).add_point(10)])

        self.assertEqual(result, expected)

    def test_vote(self):
        voter = Player(self.new_discord_user(0))
        voted_player = Player(self.new_discord_user(1))

        game = self.game.join(voter).join(voted_player)

        result = game.vote(voter, voted_player)

        expected = DeathGame([
            Player(self.new_discord_user(1), voting_rights=1, votes_count=1, point=10),
            Player(self.new_discord_user(0), voting_rights=0, votes_count=0, point=10)
            ])

        self.assertEqual(result, expected)

    def test_vote_no_rights(self):
        game = self.game.join(self.player)

        game = game.vote(self.player, self.player)

        self.assertIsNone(game.vote(self.player, self.player))

    def test_fake_vote(self):
        game = self.game.join(self.player.add_fake_voting_rights(1))

        result = game.fake_vote(self.player, self.player)

        expected = DeathGame([
            Player(
                self.discord_account,
                point=10,
                voting_rights=1,
                fake_voting_rights=0,
                votes_count=1,
                fake_votes_count=1
            )
        ])

        self.assertEqual(result, expected)

    def test_buy_voting_rights(self):
        game = self.game.join(self.player)
        result = game.buy_voting_rights(self.player)
        expected = DeathGame([
            Player(self.discord_account, point=0, voting_rights=2)
        ])

        self.assertEqual(result, expected)

    def test_buy_fake_voting_rights(self):
        game = self.game.join(self.player)
        result = game.buy_fake_voting_rights(self.player)
        expected = DeathGame([
            Player(
                self.discord_account,
                point=8,
                fake_voting_rights=1,
                voting_rights=1
            )
        ])

        self.assertEqual(result, expected)

    def test_go_to_tomorrow(self):
        not_vote_player = Player(self.new_discord_user(0))
        first_place_player = Player(self.new_discord_user(1))
        common_player = Player(self.new_discord_user(2))

        game = self.game.join(not_vote_player).join(first_place_player).join(common_player)

        result = game.vote(common_player, first_place_player).go_to_tomorrow()
        expected = DeathGame([Player(
            self.new_discord_user(2), voting_rights=1, point=10
        )])

        self.assertEqual(result, expected)

    def test_update_player(self):
        game = self.game.join(self.player)

        result = game.update_player(self.player, self.player.add_point(1))
        expected = DeathGame([self.player.add_point(1)])

        self.assertEqual(result, expected)

    def test_player_by_discord(self):
        self.game = self.game.join(self.player)

        result = self.game.player_by_discord(self.discord_account)
        self.assertEqual(result, self.player.add_voting_rights(1).add_point(10))

    def test_votes_ranking(self):
        voter = Player(self.new_discord_user(0))
        voted_player = Player(self.new_discord_user(1))

        game = self.game.join(voter).join(voted_player)
        game = game.vote(voter, voted_player)

        ranking = game.votes_ranking()
        expected = [
            voted_player.add_voting_rights(1).add_point(10).voted(),
            voter.add_voting_rights(1).add_point(10).vote()
        ]

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
