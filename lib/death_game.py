import discord


class DeathGame:
    def __eq__(self, other):
        return self.player_list == other.player_list

    def __init__(self, player_list=[]):
        self.player_list = player_list

    def join(self, player):
        if self.player_by_discord(player.discord_account) is not None:
            return self

        return DeathGame(self.player_list + [player])

    def vote(self, voter, voted_player):
        if not voter.has_voting_rights():
            return None

        return DeathGame([
          voter.vote(),
          voted_player.voted()
        ])

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
