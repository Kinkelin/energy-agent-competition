from enum import Enum


class Vegetation(Enum):
    # Vegetation = id, energy_value, fruit_spawn_chance,
    NONE = 127, None, None
    TREE = 0, None, 0.12
    SEQUOIA = 1, None, 0.20
    FRUIT = 2, 20, None
    BUSH = 3, 30, None
    FERN = 4, 15, None
    CACTUS = 5, 10, None

    def __new__(cls, *args):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        obj.energy_value = args[1]
        obj.fruit_spawn_chance = args[2]
        return obj