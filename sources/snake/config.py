import pygame

CELL_SIZE = 20
FPS = 10
LIVES = 3

SNAKE_COLORS = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 105, 180)
]

RESOLUTIONS = [
    (800, 600),
    (1280, 720),
    (1600, 900),
    (1920, 1080)
]

CONTROL_SETS = {
    "arrows": {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)
    },
    "wasd": {
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0)
    }
}
