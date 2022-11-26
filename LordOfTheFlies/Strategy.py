class Strategy:
    def __init__(self, id, name, author, make_turn):
        self.id = id
        self.name = name
        self.author = author
        self.make_turn = make_turn
        self.energy = 0
        self.living_agents = 0
        self.score = 0
        self.total_score = 0
        self.eliminated = False

    def __str__(self):
        return self.name + " by " + self.author

    def reset(self):
        self.score = 0
        self.energy = 0
        self.eliminated = False

