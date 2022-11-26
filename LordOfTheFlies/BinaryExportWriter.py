
VERSION = "1.0.0.0"

class BinaryExportWriter:

    def __init__(self, file, strategies):
        self.file = file
        self.strategies = strategies

    def write_step(self, time, agents, vegetation):
        # Vegetation
        self.file.write(vegetation.tobytes())
        return

    def write_header(self, terrain):
        # World size
        self.file.write(terrain.shape[0].to_bytes(4, byteorder='little'))
        self.file.write(terrain.shape[1].to_bytes(4, byteorder='little'))

        # Terrain
        self.file.write(terrain.tobytes())




    def write_results(self, agents_total):
        return