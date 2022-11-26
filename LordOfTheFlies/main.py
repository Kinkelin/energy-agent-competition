import random
import os
import itertools
import importlib
import numpy as np
from enum import Enum
from datetime import datetime
from Strategy import Strategy
from World import World, get_attempt_y, get_attempt_x
from WorldGenerator import WorldGenerator
from BinaryExportWriter import BinaryExportWriter
import shutil
import gzip


# Tournament Paramenter
STRATEGY_DIRECTORY = "exampleStrats"
OUTPUT_DIRECTORY = "out"
RESULTS_FILE = "results.txt"
EXPORT_FILE = "export.binary"
NUMBER_OF_ROUNDS = 1
AGENTS_PER_STRATEGY = 500
CLEAR_OUTPUT_DIRECTORY = True


def run_competition():
    print("Run competition with " + str(NUMBER_OF_ROUNDS) + " rounds")

    strategies = read_in_strategies()
    clear_output_directory()
    sim_name = datetime.now().strftime('%d%m%Y_%H%M%S_')
    for i in range(NUMBER_OF_ROUNDS):
        print("\nStart round " + str(i+1))
        run_simulation(os.path.join(OUTPUT_DIRECTORY, sim_name + str(i)), strategies)
        print("\nRound " + str(i+1) + " result:")
        for strategy in strategies.values():
            print(str(strategy.score) + " " + str(strategy))

    print("\nCompetition result:")
    for strategy in strategies.values():
        print(str(strategy.total_score) + " " + str(strategy))


def run_simulation(out_directory, strategies):
    generator = WorldGenerator()
    world = World(generator, strategies, AGENTS_PER_STRATEGY)
    os.makedirs(out_directory, exist_ok=True)
    with open(os.path.join(out_directory, EXPORT_FILE), 'wb') as export_file:
        writer = BinaryExportWriter(export_file, strategies)
        world.simulate(writer)


def read_in_strategies():
    print("\nReading in strategies:")
    strategies = {}
    next_strategy_id = 0
    for file in os.listdir(STRATEGY_DIRECTORY):
        if file.endswith(".py"):
            module = importlib.import_module(STRATEGY_DIRECTORY + "." + file[:-3])
            strategy = Strategy(next_strategy_id, module.get_name(), module.get_author(), module.make_turn)
            strategies[strategy.id] = strategy
            print(strategy)
            next_strategy_id += 1
    return strategies


def clear_output_directory():
    if CLEAR_OUTPUT_DIRECTORY:
        print("\nClear output directory")
        if os.path.exists(OUTPUT_DIRECTORY):
            shutil.rmtree(OUTPUT_DIRECTORY)
        os.makedirs(OUTPUT_DIRECTORY)


if __name__ == '__main__':
    run_competition()


