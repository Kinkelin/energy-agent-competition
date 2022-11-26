import random

def make_turn(world, self, memory):
    movement = [random.randint(-3,3), random.randint(-3,3)]
    do_split = random.random() < 0.01
    split_memory = None
    chase_target = -1
    return movement, do_split, split_memory, chase_target, memory

def get_name():
    return "Monkey2"

def get_author():
    return "Example"