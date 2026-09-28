class Team:

    def __init__(self, name):

        self.name = name

        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

        self.points = 0

        self.score_for = 0
        self.score_against = 0
        self.score_difference = 0

    def to_dict(self):

        return {
            "name": self.name,
            "played": self.played,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "points": self.points,
            "score_for": self.score_for,
            "score_against": self.score_against,
            "score_difference": self.score_difference
        }

    @classmethod
    def from_dict(cls, data):

        team = cls(data["name"])

        team.played = data["played"]
        team.wins = data["wins"]
        team.draws = data["draws"]
        team.losses = data["losses"]

        team.points = data["points"]

        team.score_for = data["score_for"]
        team.score_against = data["score_against"]
        team.score_difference = data["score_difference"]

        return team