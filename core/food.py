import random
from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.respawn([])

    def respawn(self, snake_body):
        max_x = (WINDOW_WIDTH // GRID_SIZE) - 1
        max_y = (WINDOW_HEIGHT // GRID_SIZE) - 1

        while True:
            self.position = (random.randint(0, max_x), random.randint(0, max_y))
            if self.position not in snake_body:
                break