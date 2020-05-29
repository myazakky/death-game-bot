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
