import numpy as np
from Vegetation import Vegetation
from Terrain import Terrain
import random

VEGETATION_CYCLE_DURATION = 100 # how long it takes to regrow bushes and ferns (during sim run the spawn chance will be divided by this constant)

FRUIT_SPAWN_RATES = {}
FRUIT_SPAWN_RATES[Vegetation.TREE.value] = 0.080
FRUIT_SPAWN_RATES[Vegetation.SEQUOIA.value] = 0.160

SPAWN_RATES = {}
for t in Terrain:
    SPAWN_RATES[t.value] = {}

SPAWN_RATES[Terrain.PLAIN.value][Vegetation.TREE.value] = 0.025
SPAWN_RATES[Terrain.PLAIN.value][Vegetation.BUSH.value] = 0.120

SPAWN_RATES[Terrain.JUNGLE.value][Vegetation.TREE.value] = 0.030
SPAWN_RATES[Terrain.JUNGLE.value][Vegetation.SEQUOIA.value] = 0.020
SPAWN_RATES[Terrain.JUNGLE.value][Vegetation.BUSH.value] = 0.150
SPAWN_RATES[Terrain.JUNGLE.value][Vegetation.FERN.value] = 0.200

SPAWN_RATES[Terrain.MOUNTAIN.value][Vegetation.TREE.value] = 0.015
SPAWN_RATES[Terrain.MOUNTAIN.value][Vegetation.BUSH.value] = 0.050

SPAWN_RATES[Terrain.DESERT.value][Vegetation.BUSH.value] = 0.005
SPAWN_RATES[Terrain.DESERT.value][Vegetation.CACTUS.value] = 0.010

class WorldGenerator:

    def __init__(self):
        self.probabilities = []
        aggregated_probability = 0
        for k1, v1 in SPAWN_RATES.items():
            for k2, v2 in v1.items():
                if k2 != Vegetation.TREE.value and k2 != Vegetation.SEQUOIA.value:
                    step_probability = v2 / VEGETATION_CYCLE_DURATION
                    self.probabilities.append([k1, k2, aggregated_probability, aggregated_probability+step_probability])
                    aggregated_probability += step_probability

        self.fruit_probabilities = []
        for k,v in FRUIT_SPAWN_RATES.items():
            self.fruit_probabilities.append([k, aggregated_probability, aggregated_probability + v])
            aggregated_probability += v

        self.gen_probabilities = []
        aggregated_probability = 0
        for k1, v1 in SPAWN_RATES.items():
            for k2, v2 in v1.items():
                self.gen_probabilities.append([k1, k2, aggregated_probability, aggregated_probability+v2])
                aggregated_probability += v2


    def generate_terrain(self, world_size):
        self.indices = np.indices(world_size)
        return np.random.randint(low=0, high=4, size=world_size, dtype=np.dtype('int8'))

    def generate_vegetation(self, terrain):
        vegetation = np.full_like(terrain, Vegetation.NONE.value)
        r = np.random.random_sample(terrain.shape)
        for p in self.gen_probabilities:
            vegetation[(terrain == p[0]) & (r >= p[2]) & (r < p[3])] = p[1]

        trees = self.indices[:,vegetation == Vegetation.TREE.value]
        self.fruit_area = {}
        self.fruit_area[Vegetation.TREE.value] = np.full(terrain.shape, False)
        for i in range(trees.shape[1]):
            for x in range(-3,4):
                for y in range(-3,4):
                    self.fruit_area[Vegetation.TREE.value][clamp(trees[0,i]+x,0,terrain.shape[0]-1),clamp(trees[1,i]+y,0,terrain.shape[1]-1)] = True

        sequoias = self.indices[:,vegetation == Vegetation.SEQUOIA.value]
        self.fruit_area[Vegetation.SEQUOIA.value] = np.full(terrain.shape, False)
        for i in range(sequoias.shape[1]):
            for x in range(-3,4):
                for y in range(-3,4):
                    self.fruit_area[Vegetation.SEQUOIA.value][clamp(sequoias[0,i]+x,0,terrain.shape[0]-1),clamp(sequoias[1,i]+y,0,terrain.shape[1]-1)] = True

        return vegetation, trees, sequoias

    def update_vegetation(self, terrain, vegetation):
        self.empty = vegetation == Vegetation.NONE.value
        self.r = np.random.random_sample(terrain.shape)
        for p in self.probabilities:
            vegetation[self.empty & (terrain == p[0]) & (self.r >= p[2]) & (self.r < p[3])] = p[1]

    def spawn_fruits(self, vegetation):
        for fp in self.fruit_probabilities:
            vegetation[self.empty & self.fruit_area[fp[0]] & (self.r >= fp[1]) & (self.r < fp[2])] = Vegetation.FRUIT.value

    def spawn_fruits2(self, terrain, vegetation):
        # clipping only works with squared worlds
        r_pos = np.random.randint(low=-3, high=4, size=(2, terrain.shape[0], terrain.shape[1]))
        fruit_pos = np.clip(r_pos + self.indices,0,terrain.shape[0]-1)
        for fp in self.fruit_probabilities:
            filter = (vegetation == fp[0]) & (self.r >= fp[1]) & (self.r < fp[2]) # tree and probability fits
            fx = fruit_pos[0,filter]
            fy = fruit_pos[1, filter]
            empty_at_fruit_pos = vegetation[fx,fy] == Vegetation.NONE.value
            vegetation[fx[empty_at_fruit_pos],fy[empty_at_fruit_pos]] = Vegetation.FRUIT.value


    # fruit spawning with loop approach, performance is slightly worse compared to full numpy approach
    # depending on the frequency of trees this might become optimal again
    def spawn_fruits3(self, terrain, vegetation, trees, sequoias):
        empty = vegetation == Vegetation.NONE.value
        r = np.random.random_sample(terrain.shape)
        for p in self.probabilities:
            vegetation[empty & (terrain == p[0]) & (r >= p[2]) & (r < p[3])] = p[1]
        all_trees = np.concatenate((trees ,sequoias), axis=1)
        for i in range(all_trees.shape[1]):
            tx = all_trees[0,i]
            ty = all_trees[1,i]
            if random.random() < FRUIT_SPAWN_RATES[vegetation[tx,ty]]:
                fruit_x = clamp(tx + random.randint(-3,3),0,terrain.shape[0]-1)
                fruit_y = clamp(ty + random.randint(-3,3),0,terrain.shape[1]-1)
                if vegetation[fruit_x,fruit_y] == Vegetation.NONE.value:
                    vegetation[fruit_x,fruit_y] = Vegetation.FRUIT.value




def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))