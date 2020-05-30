class Player:
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.discord_account == other.discord_account and
                self.votes_count == other.votes_count and
                self.fake_votes_count == other.fake_votes_count and
                self.voting_rights == other.voting_rights and
                self.fake_voting_rights == other.fake_voting_rights and
                self.point == other.point and
                self.guessed == other.guessed)

    def __init__(
        self,
        discord_account,
        votes_count=0,
        fake_votes_count=0,
        voting_rights=0,
        fake_voting_rights=0,
        point=0,
        guessed=None
    ):
        self.discord_account = discord_account
        self.votes_count = votes_count
        self.fake_votes_count = fake_votes_count
        self.voting_rights = voting_rights
        self.fake_voting_rights = fake_voting_rights
        self.point = point
        self.guessed = guessed

    def voted(self):
        return self.update(votes_count=self.votes_count + 1)

    def has_voting_rights(self):
        return self.voting_rights > 0

    def has_fake_voting_rights(self):
        return self.fake_voting_rights > 0

    def vote(self):
        if not self.has_voting_rights():
            return None

        return self.update(voting_rights=self.voting_rights - 1)

    def fake_vote(self):
        if not self.has_fake_voting_rights():
            return None

        return self.update(fake_voting_rights=self.fake_voting_rights - 1)

    def fake_voted(self):
        return self.voted().update(
            fake_votes_count=self.fake_votes_count + 1
        )

    def guess(self, target):
        if self.guessed is None:
            return self.update(guessed=target)

    def add_point(self, point):
        return self.update(point=self.point + point)

    def use_point(self, point):
        if point <= self.point:
            return self.update(point=self.point - point)

    def add_voting_rights(self, number):
        return self.update(voting_rights=self.voting_rights + number)

    def add_fake_voting_rights(self, number):
        return self.update(fake_voting_rights=self.fake_voting_rights + number)

    def update(self, **status):
        return Player(
            status.get('discord_account', self.discord_account),
            status.get('votes_count', self.votes_count),
            status.get('fake_votes_count', self.fake_votes_count),
            status.get('voting_rights', self.voting_rights),
            status.get('fake_voting_rights', self.fake_voting_rights),
            status.get('point', self.point),
            status.get('guessed', self.guessed)
        )
