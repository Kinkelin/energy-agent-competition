
VERSION = "1.0.0.0"

class BinaryExportWriter:

    def __init__(self, file, strategies):
        self.file = file
        self.strategies = strategies

    def write_step(self, time, agents, vegetation):
        return

    def write_header(self, terrain):
        print(terrain)
        self.file.write(terrain.tobytes())


    def write_results(self, agents_total):
        return