import numpy as np
from Terrain import Terrain
from Agent import Agent
from Vegetation import Vegetation
from ExportWriter import ExportWriter
from tqdm import tqdm
import random
import sys
from time import time

# PARAMETERS

WORLD_MAX_AGE = 1000
WORLD_SIZE = (512, 512)

# If True agents can walk around the world, if False they are boxed in
# For Now Only False is implemented
WORLD_WRAP = False

AGENT_STARTING_ENERGY = 100
AGENT_ENERGY_LOSS_STATIC = 0.5  # Static energy loss per step
AGENT_ENERGY_LOSS_DYNAMIC = 0.01  # Portion of current energy lost each step
MOVE_BASE_COST = 1
MOVE_COST_DIST_FACTOR = 2 # MOVE_BASE_COST * ((x+y)**MOVE_COST_DIST_FACTOR)
PLAYER_MOVE_RANGE = 3

class World:

    def __init__(self, generator, strategies, agents_per_strategy):
        print("Generating world with dimensions " + str(WORLD_SIZE))
        self.generator = generator
        self.terrain = generator.generate_terrain(WORLD_SIZE)
        self.vegetation, self.trees, self.sequoias = generator.generate_vegetation(self.terrain)
        self.agent_position = np.full(WORLD_SIZE, -1, dtype=np.int32)  # potentially np.dtype('uint16') is enough
        self.temp_agent_pos = np.copy(self.agent_position)
        self.agents = {}
        self.agents_total = 0  # total number of agents, alive or dead. Used for new agent ids
        self.strategies = strategies

        for strategy in strategies.values():
            starting_memory = {}
            for i in range(agents_per_strategy):
                id = self.agents_total
                x = random.randrange(WORLD_SIZE[0]-1)
                y = random.randrange(WORLD_SIZE[0]-1)
                self.agent_position[x,y] = id
                self.agents[id] = Agent(id, x, y, strategy.id, AGENT_STARTING_ENERGY, starting_memory)
                self.agents_total += 1

        self.dead_agents = []
        self.remaining_strategies_nr = len(strategies)
        self.age = 0

        # performance tracking
        self.t_make_turn = 0
        self.t_agent_pos_setup = 0
        self.t_agent_movement = 0
        self.t_chase_movement = 0
        self.t_eat_vegetation = 0
        self.t_energy_calculation = 0
        self.t_strategy_calculation = 0
        self.t_spawn_vegetation = 0
        self.t_spawn_fruits = 0
        self.t_export_writer = 0


    # STEP


    def step(self):
        t = time()

        # collect and store agent decisions
        for agent in self.agents.values():
            agent.actions = self.strategies[agent.strategy_id].make_turn(self, agent, agent.actions[4])

        self.t_make_turn += time() - t
        t = time()

        # setup temp agent positions
        np.copyto(self.temp_agent_pos,self.agent_position)

        # clear position array
        self.agent_position.fill(-1)

        self.t_agent_pos_setup += time() - t
        t = time()

        # move players one by one into new array, store chasers in separate list for later
        # if moving onto team mate, marge
        # if moving onto enemy -> battle
        # energy costs are calculated with move
        # dead players get stored in extra list
        # move chasers. If chased target is part of chasers don't resolve last.
        chasers = []
        for agent in list(self.agents.values()):
            if not agent.dead:
                agent.old_x = agent.x
                agent.old_y = agent.y

                if agent.actions[1]:  # split
                    agent.energy /= 2
                    new_agent = Agent(self.agents_total, agent.old_x, agent.old_y, agent.strategy_id, agent.energy, agent.actions[2])
                    self.agents[new_agent.id] = new_agent
                    self.agent_to_pos(new_agent,0,0)
                    self.agents_total += 1

                if agent.actions[3] >= 0:  # chase
                    chasers.append(agent)
                else: # move normally
                    self.agent_to_pos(agent, agent.actions[0][0], agent.actions[0][1])

        self.t_agent_movement += time() - t
        t = time()

        # move chasers not in a deadlock
        for agent in chasers.copy():
            if not agent.dead and not agent.actions[3] in self.dead_agents and self.agents[agent.actions[3]].actions[3] < 0:
                cx,cy = get_chase_movement(agent, self.agents[agent.actions[3]])
                self.agent_to_pos(agent, cx, cy)
                chasers.remove(agent)

        # move remaining chasers
        for agent in chasers:
            if not agent.dead and not agent.actions[3] in self.dead_agents:
                cx,cy = get_chase_movement(agent, self.agents[agent.actions[3]])
                self.agent_to_pos(agent, cx, cy)

        self.t_chase_movement += time() - t
        t = time()

        # energy cost calculation
        for agent in self.agents.values():
            idle_cost = AGENT_ENERGY_LOSS_STATIC + agent.energy * AGENT_ENERGY_LOSS_DYNAMIC
            move_cost = MOVE_BASE_COST * ((abs(agent.x - agent.old_x)+abs(agent.y-agent.old_y))**MOVE_COST_DIST_FACTOR)
            agent.energy -= (idle_cost + move_cost)
            if agent.energy <= 0:
                agent.dead = True
                self.agent_position[agent.x,agent.y] = -1
                self.dead_agents.append(agent)
                del self.agents[agent.id]
            break

        self.t_energy_calculation += time() - t
        t = time()

        # clear strategy energy counts
        for strategy in self.strategies.values():
            strategy.energy = 0

        self.t_strategy_calculation += time() - t
        t = time()

        # eat vegetation and update scores
        for agent in self.agents.values():
            # eat vegetation
            veg = Vegetation(self.vegetation[agent.x,agent.y])
            if veg.energy_value is not None:
                agent.energy += veg.energy_value
                self.vegetation[agent.x,agent.y] = Vegetation.NONE.value;

            # update scores
            strategy = self.strategies[agent.strategy_id]
            strategy.energy += agent.energy
            strategy.score += agent.energy
            strategy.total_score += agent.energy

        self.t_eat_vegetation += time() - t
        t = time()

        # spawn new vegetation
        self.generator.update_vegetation(self.terrain, self.vegetation)

        self.t_spawn_vegetation += time() - t
        t = time()

        self.generator.spawn_fruits(self.vegetation)
        #self.generator.spawn_fruits2(self.terrain, self.vegetation)

        self.t_spawn_fruits += time() - t
        t = time()

        # calculate metadata

        # calculate eliminations
        for strategy in self.strategies.values():
            strategy.eliminated = True
            strategy.living_agents = 0

        for agent in self.agents.values():
            self.strategies[agent.strategy_id].eliminated = False
            self.strategies[agent.strategy_id].living_agents += 1

        # calculate number of remaining strategies
        self.remaining_strategies_nr = 0
        for strategy in self.strategies.values():
            if not strategy.eliminated:
                self.remaining_strategies_nr += 1

        self.t_strategy_calculation += time() - t

        self.age += 1

        # return if simulation is finished
        return self.remaining_strategies_nr <= 1

    def agent_to_pos(self, agent, move_x, move_y):

        # calculate new position
        x = clamp(agent.x + move_x, 0, WORLD_SIZE[0]-1)
        y = clamp(agent.x + move_y, 0, WORLD_SIZE[1]-1)

        if self.agent_position[x,y] < 0:
            # destination field free, good to go
            self.agent_position[x,y] = agent.id
            agent.x = x
            agent.y = y
        else:
            other = self.agents[self.agent_position[x][y]]
            if other.strategy_id != agent.strategy_id:
                # enemy found, fight
                agent.x = x
                agent.y = y

                self.agent_position[x,y] = -1

                agent.energy -= other.energy
                agent_dead = False
                if agent.energy > 0:
                    self.agent_position[x,y] = agent.id
                else:
                    agent.dead = True
                    self.dead_agents.append(agent)
                    del self.agents[agent.id]
                    agent_dead = True

                other.energy -= agent.energy
                if other.energy > 0:
                    self.agent_position[x,y] = other.id
                else:
                    other.dead = True
                    self.dead_agents.append(other)
                    del self.agents[other.id]
                    if agent_dead:
                        self.agent_position[x,y] = -1

            else:
                # teammate found, merge together
                if agent.energy >= other.energy:
                    self.agent_position[x,y] = agent.id
                    agent.energy += other.energy
                    other.energy = 0
                    other.dead = True
                    self.dead_agents.append(other)
                    del self.agents[other.id]
                else:
                    other.energy += agent.energy
                    agent.energy = 0
                    agent.dead = True
                    self.dead_agents.append(agent)
                    del self.agents[agent.id]


    def simulate(self, writer):
        t = time()
        writer.write_header(self.terrain, self.vegetation)
        writer.write_step(self.age, self.agents, self.vegetation, self.vegetation) # step 0, initial situation
        self.t_export_writer += time() - t
        print("Run simulation steps:")
        for i in tqdm(range(WORLD_MAX_AGE),file=sys.stdout):
            old_vegetation = np.copy(self.vegetation)
            finished = self.step()
            t = time()
            writer.write_step(self.age, self.agents, self.vegetation, old_vegetation)
            self.t_export_writer += time() - t
            if finished:
                break
        t = time()
        writer.write_results()
        self.t_export_writer += time() - t

        print("t_make_turn", self.t_make_turn)
        print("t_agent_pos_setup", self.t_agent_pos_setup)
        print("t_agent_movement", self.t_agent_movement)
        print("t_chase_movement", self.t_chase_movement)
        print("t_eat_vegetation", self.t_eat_vegetation)
        print("t_energy_calculation", self.t_energy_calculation)
        print("t_strategy_calculation", self.t_strategy_calculation)
        print("t_spawn_vegetation", self.t_spawn_vegetation)
        print("t_spawn_fruits", self.t_spawn_fruits)
        print("t_export_writer", self.t_export_writer)

def agent_to_pos_old(self, agent, move_x, move_y, previous_attempts=0):

        # calculate new position
        x = clamp(agent.x + move_x + get_attempt_x(previous_attempts), 0, WORLD_SIZE[0]-1)
        y = clamp(agent.x + move_y+ get_attempt_y(previous_attempts), 0, WORLD_SIZE[1]-1)
        if previous_attempts > 10:
            print("agent_to_pos", agent, move_x, move_y, x, y, previous_attempts)

        if self.agent_position[x][y] < 0:
            # destination field free, good to go
            self.agent_position[x][y] = agent.id
            agent.x = x
            agent.y = y
        else:
            other = self.agents[self.agent_position[x][y]]
            if other.strategy_id != agent.strategy_id:
                # enemy found, fight
                agent.x = x
                agent.y = y

                self.agent_position[x][y] = -1

                agent.energy -= other.energy
                if agent.energy > 0:
                    self.agent_position[x][y] = agent.id
                else:
                    agent.dead = True
                    self.dead_agents.append(agent)
                    del self.agents[agent.id]

                other.energy -= agent.energy
                if other.energy > 0:
                    self.agent_position[x][y] = other.id
                else:
                    other.dead = True
                    self.dead_agents.append(other)
                    del self.agents[other.id]

            else:
                # teammate found, go to another nearby position instead
                self.agent_to_pos(agent, move_x, move_y, previous_attempts+1)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def get_attempt_x(attempt):
    return (((attempt+1) % 3) - 1) * (attempt // 9 + 1)

def get_attempt_y(attempt):
    return ((((attempt//3)+1) % 3) - 1) * (attempt // 9 + 1)

def get_chase_movement(chaser, target):
    return clamp(target.x-chaser.x,-3,3),clamp(target.y-chaser.y,-3,3)

