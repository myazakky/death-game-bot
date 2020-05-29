class DeathGame:
    def __eq__(self, other):
        return self.player_list == other.player_list

    def __init__(self, player_list=[]):
        self.player_list = player_list

    def join(self, player):
        return DeathGame(self.player_list + [player])
