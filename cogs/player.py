class Player:
    def __eq__(self, other):
        return (self.discord_account == other.discord_account and
                self.votes_count == other.votes_count)

    def __init__(self, discord_account, votes_count=0):
        self.discord_account = discord_account
        self.votes_count = votes_count

    def voted(self):
        return Player(
            self.discord_account,
            votes_count=self.votes_count + 1,
        )
