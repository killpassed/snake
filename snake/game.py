import pygame
from snake.snake import Snake
from snake.food import Food
from snake.menu import Menu
from snake.config import CELL_SIZE, RESOLUTIONS, FPS, LIVES, CONTROL_SETS, SNAKE_COLORS
from snake.utils import load_settings, save_settings
from snake.strings import STRINGS

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake by killpassed")
        self.settings = load_settings()
        self.apply_resolution()
        self.clock = pygame.time.Clock()
        self.snake_color = SNAKE_COLORS[self.settings["snake_color"]]
        self.reset()

    def apply_resolution(self):
        res = RESOLUTIONS[self.settings["resolution"]]
        flags = pygame.FULLSCREEN if self.settings["fullscreen"] else 0
        self.width, self.height = res
        self.grid_width = self.width // CELL_SIZE
        self.grid_height = self.height // CELL_SIZE
        self.screen = pygame.display.set_mode(res, flags)

    def reset(self):
        self.snake = Snake(self.grid_width, self.grid_height, self.snake_color)
        self.food = Food(self.grid_width, self.grid_height)
        self.lives = LIVES
        self.score = 0
        self.controls = CONTROL_SETS[self.settings["controls"]]

    def run(self):
        pygame.mouse.set_visible(False)
        while True:
            menu = Menu(self)
            action = menu.run()
            if action == "quit": break
            if action == "play": self.game_loop()

    def game_loop(self):
        s = STRINGS[self.settings["language"]]
        running = True
        while running:
            self.clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT: return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: return
                    if e.key == pygame.K_F11:
                        self.settings["fullscreen"] = not self.settings["fullscreen"]
                        self.apply_resolution()
                    elif e.key in self.controls:
                        self.snake.change_direction(self.controls[e.key])
            self.snake.move()
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.randomize()
                self.score += 1
            if self.snake.check_collision():
                self.lives -= 1
                if self.lives == 0: return
                self.snake = Snake(self.grid_width, self.grid_height, self.snake_color)
            self.draw_game(s)

    def draw_game(self, s):
        self.screen.fill((0, 0, 0))
        if self.settings["show_grid"]:
            for x in range(0, self.width, CELL_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.height))
            for y in range(0, self.height, CELL_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.width, y))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        font = pygame.font.SysFont("arial", 28, True)
        lives = font.render(f"{s['lives']}: {self.lives}", True, (255, 255, 255))
        score = font.render(f"{s['score']}: {self.score}", True, (255, 255, 255))
        self.screen.blit(lives, (10, 10))
        self.screen.blit(score, (10, 40))
        control_hint = "WASD" if self.settings["controls"] == "wasd" else "↑↓←→"
        ctrl_text = font.render(control_hint + " / ESC", True, (100, 100, 100))
        self.screen.blit(ctrl_text, (self.width - 200, self.height - 40))
        pygame.display.flip()
