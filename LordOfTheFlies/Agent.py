class Agent:
    def __init__(self, id, x, y, strategy_id, energy, memory):
        self.id = id
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.strategy_id = strategy_id
        self.energy = energy
        self.dead = False

        # actions for the current step and the memory that is passed back to the agent in the next step
        self.actions = ([0,0], False, None, -1, memory) # movement, do_split, split_memory, chase_target, memory

