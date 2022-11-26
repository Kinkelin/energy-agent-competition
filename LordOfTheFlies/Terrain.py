from enum import Enum

class Terrain(Enum):
    # Terrain = id, energy_cost
    PLAIN = 0, 1
    JUNGLE = 1, 2
    MOUNTAIN = 2, 3
    DESERT = 3, 4

    def __new__(cls, *args):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        obj.energy_cost = args[1]
        return obj