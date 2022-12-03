import tkinter as tk
from tkinter import filedialog


def read_short(file):
    return int.from_bytes(file.read(2), "little")

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)
with open(file_path, "rb") as file:
    title = file.read(64)
    print(title)
    version = read_short(file)
    print(version)
    world_size = [read_short(file), read_short(file)]
    print(world_size)
    print(int.from_bytes(file.read(4), "little"))
    print(int.from_bytes(file.read(4), "little"))
    file.read(world_size[0]*world_size[1]*4-12)
    print(int.from_bytes(file.read(4), "little"))
    print(int.from_bytes(file.read(4), "little", signed=True))
    print(int.from_bytes(file.read(4), "little", signed=True))

