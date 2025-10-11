import pygame
from snake.config import CELL_SIZE

class Snake:
    def __init__(self, grid_width, grid_height, color):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.color = color
        self.body = [(grid_width // 2, grid_height // 2)]
        self.direction = (1, 0)
        self.grow_flag = False

    def change_direction(self, direction):
        if (direction[0] == -self.direction[0] and direction[1] == -self.direction[1]):
            return
        self.direction = direction

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def check_collision(self):
        x, y = self.body[0]
        return (
            x < 0 or x >= self.grid_width or
            y < 0 or y >= self.grid_height or
            self.body[0] in self.body[1:]
        )

    def draw(self, surface):
        for x, y in self.body:
            pygame.draw.rect(surface, self.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
