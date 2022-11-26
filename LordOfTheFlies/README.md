# Lord Of The Flies Group Simulation
This repository houses the engine for our [lord of the flies simulation](https://docs.google.com/document/d/15APhBIm-rgxk6GXQKCO1vkKENLqWDIkzNchoZifImVE). This simulation is a sequel to [karykh's prisoner's dilema tournament]() and hosted by the [prisoner's dilema enjoyers github organization]().

## Running
The engine comes with a few example strategies in the exampleStrats folder. To create your own strategy, place a new file in that folder and fill it with the following contents.

```python
def make_turn(world, self, memory):
    movement = None
    do_split = False
    split_memory = None
    chase_target = None
    return movement, do_split, split_memory, chase_target, memory
```
Any changes you make to the function define your strategy.
