import discord


class DeathGame:
    def __eq__(self, other):
        return self.player_list == other.player_list

    def __init__(self, player_list=[]):
        self.player_list = player_list

    def join(self, player):
        if self.player_by_discord(player.discord_account) is not None:
            return self

        return DeathGame(self.player_list + [
            player.add_voting_rights(1).add_fake_voting_rights(1).add_point(10)
        ])

    def leave(self, player):
        return DeathGame(
            [p for p in self.player_list if p != player]
        )

    def guess(self, guesser, target):
        guesser = self.player_by_discord(guesser.discord_account)
        target = self.player_by_discord(target.discord_account)

        if guesser.guessed is None:
            return self.update_player(guesser, guesser.guess(target))

    def vote(self, voter, voted_player):
        voter = self.player_by_discord(voter.discord_account)

        if not voter.has_voting_rights():
            return None

        lost_voting_rights_game = self.update_player(voter, voter.vote())
        voted_player = lost_voting_rights_game.player_by_discord(
            voted_player.discord_account
        )  # 投票者と被投票者が同一人物だった場合も考慮して、このような処理にしている。
        return lost_voting_rights_game.update_player(
            voted_player, voted_player.voted()
        )

    def fake_vote(self, voter, voted_player):
        voter = self.player_by_discord(voter.discord_account)

        if not voter.has_fake_voting_rights():
            return None

        lost_voting_rights_game = self.update_player(voter, voter.fake_vote())
        voted_player = lost_voting_rights_game.player_by_discord(
            voted_player.discord_account
        )  # 投票者と被投票者が同一人物だった場合も考慮して、このような処理にしている。
        return lost_voting_rights_game.update_player(
            voted_player, voted_player.fake_voted()
        )

    def buy_voting_rights(self, buyer):
        buyer = self.player_by_discord(buyer.discord_account)

        if buyer.point >= 10:
            return self.update_player(
                buyer,
                buyer.use_point(10).add_voting_rights(1)
            )

    def buy_fake_voting_rights(self, buyer):
        buyer = self.player_by_discord(buyer.discord_account)

        if buyer.point >= 2:
            return self.update_player(
                buyer,
                buyer.use_point(2).add_fake_voting_rights(1)
            )

    def let_first_place_players_leave(self):
        most_votes_count = self.real_votes_ranking()[0].votes_count

        first_place_players = [
            p for p in self.player_list if p.votes_count - p.fake_votes_count == most_votes_count
        ]

        clear_game = self
        for player in first_place_players:
            clear_game = clear_game.leave(player)

        return clear_game

    def let_not_voted_players_leave(self):
        not_voted_players = [
            p for p in self.player_list if p.voting_rights > 0
        ]

        voted_players_only_game = self
        for player in not_voted_players:
            voted_players_only_game = voted_players_only_game.leave(player)

        return voted_players_only_game

    def initialize_players(self):
        initialized_players_game = self

        for player in self.player_list:
            initialized_players_game = initialized_players_game.update_player(
                player, player.add_voting_rights(1).update(
                    votes_count=0, fake_votes_count=0, guessed=None
                )
            )

            if player.fake_voting_rights <= 0:
                initialized_players_game = initialized_players_game.update_player(
                    player, player.add_fake_voting_rights(1)
                )

        return initialized_players_game

    def add_point_to_guessed_right(self):
        most_votes_count = self.real_votes_ranking()[0].votes_count
        first_place_accounts = [
            p.discord_account for p in self.player_list if p.votes_count - p.fake_votes_count == most_votes_count
        ]

        added_game = self
        for player in self.player_list:
            if player.guessed is None:
                continue

            if player.guessed.discord_account in first_place_accounts:
                added_game = added_game.update_player(
                    player, player.add_point(1)
                )

        return added_game

    def go_to_tomorrow(self):
        tomorrow_game = self.add_point_to_guessed_right(
            ).let_first_place_players_leave(
            ).let_not_voted_players_leave(
            ).initialize_players()

        return tomorrow_game

    def update_player(self, player, updated_player):
        player = self.player_by_discord(player.discord_account)

        if player is not None:
            other_players = [
                p for p in self.player_list if p != player
            ]

            return DeathGame([updated_player] + other_players)

    def player_by_discord(self, discord_account):
        discord_accounts = list(
            map(lambda p: p.discord_account, self.player_list)
        )

        if discord_account not in discord_accounts:
            return None

        return self.player_list[discord_accounts.index(discord_account)]

    def votes_ranking(self):
        return sorted(
            self.player_list,
            key=lambda p: p.votes_count,
            reverse=True
        )

    def real_votes_ranking(self):
        return sorted(
            self.player_list,
            key=lambda p: p.votes_count - p.fake_votes_count,
            reverse=True
        )

    def embed_votes_ranking(self):
        embed = discord.Embed(title='得票数ランキング')
        ranking = self.votes_ranking()

        for rank, player in enumerate(ranking):
            if player.votes_count <= 0:
                break

            embed.add_field(
                name=f'{rank + 1}位',
                value=f'{player.discord_account.mention}: {player.votes_count}票'
            )

        return embed

    def embed_real_votes_ranking(self):
        embed = discord.Embed(title='本当の得票数ランキング')
        ranking = self.real_votes_ranking()

        for rank, player in enumerate(ranking):
            if player.votes_count - player.fake_votes_count <= 0:
                break

            embed.add_field(
                name=f'{rank + 1}位',
                value=f'{player.discord_account.mention}: {player.votes_count - player.fake_votes_count}票'
            )

        return embed
