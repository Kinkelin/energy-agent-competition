import numpy as np

# Parameters
VERSION = "1.0.0.0"
SEPARATOR = ";"
"""
Text file export works in theory, but creates GB sized files. Binary files should be far better for our purposes.
"""
class ExportWriter:

    def __init__(self, file, strategies):
        self.file = file
        self.strategies = strategies
        np.set_printoptions(threshold=np.inf)

    def write_line(self, *text):
        print(SEPARATOR.join(map(str, text)), file=self.file)
        #self.file.write(SEPARATOR.join(map(str, text)).encode())
        #print(*text, file=self.file, sep=SEPARATOR)   # twice as slow

    def write_step(self, time, agents, vegetation):
        line_content = ["TIME", time]
        self.write_line("VEGETATION", format_array(vegetation))
        for agent in agents.values():
            line_content.extend(["AGENT",agent.id])
            line_content.extend(["X",agent.x])
            line_content.extend(["Y",agent.y])
            line_content.extend(["S",agent.strategy_id])
            line_content.extend(["E",agent.energy])
        self.write_line(*line_content)
        return

    def write_header(self, terrain):
        self.write_line("TITLE","Lord of the Flies Simulation export file")
        self.write_line("VERSION",VERSION)
        self.write_line("WORLD_SIZE", terrain.shape[0], terrain.shape[1])
        self.write_line("TERRAIN", format_array(terrain))
        self.write_line("STEPS")


    def write_results(self, agents_total):
        self.write_line("RESULTS")
        self.write_line("AGENTS_TOTAL", agents_total)

def format_array(array):
    return np.array2string(array).replace('\n', '')