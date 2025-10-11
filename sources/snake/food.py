import random
import pygame
from snake.config import CELL_SIZE

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize()

    def randomize(self):
        self.position = (
            random.randint(0, self.grid_width - 1),
            random.randint(0, self.grid_height - 1)
        )

    def draw(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, self.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
