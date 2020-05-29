class Player:
    def __eq__(self, other):
        return (self.discord_account == other.discord_account and
                self.votes_count == other.votes_count and
                self.voting_rights == other.voting_rights and
                self.point == other.point)

    def __init__(
        self,
        discord_account,
        votes_count=0,
        voting_rights=0,
        point=0,
    ):
        self.discord_account = discord_account
        self.votes_count = votes_count
        self.voting_rights = voting_rights
        self.point = point

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
          voting_rights=self.voting_rights - 1,
        )

    def add_point(self, point):
        return Player(
            self.discord_account,
            self.votes_count,
            self.voting_rights,
            self.point + point
        )

    def use_point(self, point):
        if point <= self.point:
            return Player(
                self.discord_account,
                self.votes_count,
                self.voting_rights,
                self.point - point
            )

    def add_voting_rights(self, number):
        return Player(
                self.discord_account,
                self.votes_count,
                self.voting_rights + number,
                self.point
            )
