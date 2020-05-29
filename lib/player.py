class Player:
    def __eq__(self, other):
        return (self.discord_account == other.discord_account and
                self.votes_count == other.votes_count)

    def __init__(self, discord_account, votes_count=0, voting_rights=0):
        self.discord_account = discord_account
        self.votes_count = votes_count
        self.voting_rights = voting_rights

    def voted(self):
        return Player(
            self.discord_account,
            votes_count=self.votes_count + 1,
        )

    def has_voting_rights(self):
        return self.voting_rights > 0

    def vote(self):
        if not self.has_voting_rights():
            return None

        return Player(
          self.discord_account,
          votes_count=self.votes_count,
          voting_rights=self.voting_rights,
        )
