from typing import Tuple, List, Dict
from random import randint, choice, random
from environment import WumpusWorld
class MovingWumpusModule:
    def __init__(self, world: WumpusWorld):
        self.world = world

    def move_wumpus(self) -> Tuple[int,int] | None:
        """Move the Wumpus to a random adjacent cell.
           Return new (x,y) if moved, else None.
        """
        wumpus_positions = [(i, j) for i in range(self.world.grid_size)
                            for j in range(self.world.grid_size)
                            if self.world.world[i][j]["wumpus"]]

        if not wumpus_positions:
            return None

        wx, wy = choice(wumpus_positions)
        new_positions = [(wx + dx, wy + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        new_positions = [(nx, ny) for nx, ny in new_positions
                         if 0 <= nx < self.world.grid_size and 0 <= ny < self.world.grid_size
                         and not self.world.world[nx][ny]["pit"]
                         and not self.world.world[nx][ny]["wumpus"]]

        if new_positions:
            new_x, new_y = choice(new_positions)
            self.world.world[wx][wy]["wumpus"] = False
            self.world.world[new_x][new_y]["wumpus"] = True
            return (new_x, new_y)

        return None

    def update(self, world, ui, agent):
            self.move_wumpus()
            if hasattr(world, "update_percepts"):
                world.update_percepts()
            elif hasattr(world, "get_percepts"):
                world.percepts = world.get_percepts(world.agent_pos)

            ui._update(world, agent)   
            ui.render()               

            if hasattr(agent, "update_knowledge"):
                agent.update_knowledge(world.agent_pos, world.percepts, world)