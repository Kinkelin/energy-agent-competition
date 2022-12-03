import numpy as np

VERSION = 1

class BinaryFileWriter:

    def __init__(self, file, strategies):
        self.file = file
        self.strategies = strategies

    def write_step(self, time, agents, vegetation, old_vegetation):
        vegetation_change = np.where(vegetation != old_vegetation)
        nr_of_changes = len(vegetation_change[0])

        # Number of vegetation changes
        self.write_int(nr_of_changes)

        for i in range(nr_of_changes):
            x = vegetation_change[0][i]
            y = vegetation_change[1][i]
            new_vegetation = vegetation[x,y]

            # Vegetation Change
            self.write_short(x)
            self.write_short(y)
            self.write_byte(new_vegetation)

        nr_of_agents = len(agents)

        # Number of agents alive
        self.write_int(nr_of_agents)
        for key in agents:
            agent = agents[key]
            # Agent Information
            self.write_int(agent.id)
            self.write_short(agent.x)
            self.write_short(agent.y)
            self.write_short(agent.strategy_id)
            self.write_float(agent.energy)


    def write_header(self, terrain, vegetation):
        #terrain = terrain.copy()
       # terrain.astype(np.uint8)
       # terrain[0,0] = 17
       # terrain[1,0] = 5
       # terrain[0,1] = 5
       # terrain[511,511] = 20
       # vegetation = vegetation.copy()
       # vegetation[0,0] = 17
       # vegetation[1,0] = 5
      #  vegetation[511,511] = 20

        # Human readable title
        self.write_string("Simulation export file", 64)

        # Format version number
        self.write_short(VERSION)

        # World size
        self.write_short(terrain.shape[0])
        self.write_short(terrain.shape[1])

        # Terrain
        self.write_nparray(terrain)

        # Initial Vegetation
        self.write_nparray(vegetation)

        # Number of strategies
        self.write_short(len(self.strategies))

        # Number of agents per strategy
        self.write_short(0) # TODO pass value down from main module


    def write_results(self):
        # Results start marker
        self.write_int(-1)
        for key in self.strategies:
            strategy = self.strategies[key]

            # Strategy information
            self.write_short(strategy.id)
            self.write_float(strategy.score)
            self.write_string(strategy.name, 64)
            self.write_string(strategy.author, 64)

    def write_short(self, n):
        self.write_number(n, byte_length=2)

    def write_int(self, n, signed=True):
        self.write_number(n, byte_length=4, signed=signed)

    def write_number(self, n, byte_length, signed=False):
        self.file.write(int(n).to_bytes(byte_length, byteorder='little', signed=signed))

    def write_string(self, text, fixed_byte_length):
        self.file.write(text.ljust(fixed_byte_length)[0:fixed_byte_length].encode('ascii'))

    def write_byte(self, n, signed=True):
        self.write_number(n, byte_length=1, signed=signed)

    def write_nparray(self, nparray):
        self.file.write(nparray.tobytes())

    def write_float(self, f):
        self.file.write('{:032b}'.format(np.float32(f).view(np.int32)).encode('ascii'))