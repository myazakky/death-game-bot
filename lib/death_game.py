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
            player.add_voting_rights(1).add_point(10)
        ])

    def vote(self, voter, voted_player):
        voter = self.player_by_discord(voter.discord_account)
        voted_player = self.player_by_discord(voted_player.discord_account)

        if not voter.has_voting_rights():
            return None

        other_players = [
            p for p in self.player_list if p != voter and p != voted_player
        ]  # Remove voter and voted player.(投票者、被投票者を削除)

        return DeathGame([
          voter.vote(),
          voted_player.voted()
        ] + other_players)

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
