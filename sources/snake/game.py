import pygame
from snake.snake import Snake
from snake.food import Food
from snake.menu import Menu
from snake.config import CELL_SIZE, RESOLUTIONS, FPS, LIVES, CONTROL_SETS, SNAKE_COLORS
from snake.utils import load_settings, save_settings
from snake.strings import STRINGS
import os

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("snake by killpassed")
        self.settings = load_settings()
        self.apply_resolution()
        self.clock = pygame.time.Clock()
        self.reset()

    def apply_resolution(self):
        res = RESOLUTIONS[self.settings["resolution"]]
        flags = pygame.FULLSCREEN if self.settings.get("fullscreen") else 0
        self.width, self.height = res
        self.grid_width = max(4, self.width // CELL_SIZE)
        self.grid_height = max(4, self.height // CELL_SIZE)
        self.screen = pygame.display.set_mode(res, flags)

    def reset(self):
        self.snake_color = SNAKE_COLORS[self.settings.get("snake_color", 0)]
        self.snake = Snake(self.grid_width, self.grid_height, self.snake_color)
        self.food = Food(self.grid_width, self.grid_height)
        self.lives = LIVES
        self.score = 0
        self.highscore = self.settings.get("highscore", 0)
        self.controls = CONTROL_SETS[self.settings.get("controls", "arrows")]

    def run(self):
        pygame.mouse.set_visible(False)
        while True:
            menu = Menu(self)
            action = menu.run()
            if action == "quit":
                save_settings(self.settings)
                break
            if action == "play":
                self.reset()
                self.game_loop()

    def game_loop(self):
        s_key = self.settings.get("language", "ru")
        s = STRINGS.get(s_key, STRINGS["ru"])
        while True:
            self.clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    save_settings(self.settings)
                    return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        save_settings(self.settings)
                        return
                    if e.key == pygame.K_F11:
                        self.settings["fullscreen"] = not self.settings.get("fullscreen", False)
                        self.apply_resolution()
                    elif e.key in self.controls:
                        self.snake.change_direction(self.controls[e.key])

            self.snake.move()

            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.randomize(self.snake.body)
                self.score += 1
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.settings["highscore"] = self.highscore
                    save_settings(self.settings)

            if self.snake.check_collision():
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                    self.game_over()
                    return
                else:
                    self.snake = Snake(self.grid_width, self.grid_height, self.snake_color)

            self.draw_game()

    def draw_game(self):
        s_key = self.settings.get("language", "ru")
        s = STRINGS.get(s_key, STRINGS["ru"])
        self.screen.fill((0, 0, 0))

        if self.settings.get("show_grid"):
            for x in range(0, self.width, CELL_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.height))
            for y in range(0, self.height, CELL_SIZE):
                pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.width, y))

        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        font = pygame.font.SysFont("arial", 28, True)
        lives = font.render(f"{s['lives']}: {self.lives}", True, (255, 255, 255))
        score = font.render(f"{s['score']}: {self.score}", True, (255, 255, 255))
        highscore = font.render(f"{s['record']}: {self.highscore}", True, (255, 255, 255))

        self.screen.blit(lives, (10, 10))
        self.screen.blit(score, (10, 40))
        self.screen.blit(highscore, (10, 70))

        control_hint = "WASD" if self.settings.get("controls") == "wasd" else "↑↓←→"
        ctrl_text = font.render(control_hint + " / ESC", True, (100, 100, 100))
        self.screen.blit(ctrl_text, (self.width - ctrl_text.get_width() - 10, self.height - 40))
        pygame.display.flip()

    def game_over(self):
        s_key = self.settings.get("language", "ru")
        s = STRINGS.get(s_key, STRINGS["ru"])
        font_big = pygame.font.SysFont("arial", 72, True)
        font_small = pygame.font.SysFont("arial", 36)

        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)

        self.screen.blit(overlay, (0, 0))
        text = font_big.render(s["game_over"], True, (255, 255, 255))
        rect = text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(text, rect)

        score_text = font_small.render(f"{s['score']}: {self.score}", True, (255, 255, 255))
        high_text = font_small.render(f"{s['record']}: {self.highscore}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 2))
        self.screen.blit(high_text, (self.width // 2 - high_text.get_width() // 2, self.height // 2 + 50))

        hint = font_small.render(s["press_enter"], True, (200, 200, 200))
        self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, self.height // 2 + 150))

        pygame.display.flip()

        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        waiting = False
