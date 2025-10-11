import pygame
from snake.strings import STRINGS
from snake.config import SNAKE_COLORS, RESOLUTIONS
from snake.utils import save_settings

class Menu:
    def __init__(self, game):
        self.game = game
        self.selected = 0

    def draw_text(self, text, size, y, color=(255, 255, 255)):
        font = pygame.font.SysFont("arial", size, True)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(self.game.width // 2, y))
        self.game.screen.blit(surf, rect)

    def draw_corner_text(self, lines, color=(120, 120, 120)):
        font = pygame.font.SysFont("arial", 22)
        total_height = len(lines) * font.get_linesize()
        x = self.game.width - 10
        y = self.game.height - total_height - 10
        for i, text in enumerate(lines):
            surf = font.render(text, True, color)
            rect = surf.get_rect(bottomright=(x, y + i * font.get_linesize()))
            self.game.screen.blit(surf, rect)

    def run(self):
        pygame.mouse.set_visible(False)
        lang = self.game.settings["language"]
        s = STRINGS[lang]
        options = [s["play"], s["settings"], s["quit"]]

        while True:
            self.game.screen.fill((0, 0, 0))
            self.draw_text(s["title"], 72, self.game.height // 4, self.game.snake_color)

            for i, opt in enumerate(options):
                color = (255, 255, 255) if i == self.selected else (150, 150, 150)
                self.draw_text(opt, 40, self.game.height // 2 + i * 60, color)

            self.draw_corner_text(["version 1.0", "game by killpassed"])

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(options)
                    elif e.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(options)
                    elif e.key == pygame.K_RETURN:
                        if self.selected == 0:
                            return "play"
                        elif self.selected == 1:
                            self.settings_menu()
                        elif self.selected == 2:
                            return "quit"

    def settings_menu(self):
        s = STRINGS[self.game.settings["language"]]
        items = ["language", "controls", "color", "resolution", "grid", "fullscreen"]
        selected = 0

        while True:
            self.game.screen.fill((0, 0, 0))
            for i, key in enumerate(items):
                text = s[key]
                if key == "language":
                    val = "Русский" if self.game.settings["language"] == "ru" else "English"
                elif key == "controls":
                    val = "WASD" if self.game.settings["controls"] == "wasd" else "↑↓←→"
                elif key == "color":
                    val = str(self.game.settings["snake_color"] + 1)
                elif key == "resolution":
                    res = RESOLUTIONS[self.game.settings["resolution"]]
                    val = f"{res[0]}x{res[1]}"
                elif key == "grid":
                    val = s["on"] if self.game.settings["show_grid"] else s["off"]
                elif key == "fullscreen":
                    val = s["on"] if self.game.settings["fullscreen"] else s["off"]
                txt = f"{text}: {val}"
                color = (255, 255, 255) if i == selected else (120, 120, 120)
                self.draw_text(txt, 36, self.game.height // 3 + i * 60, color)

            self.draw_corner_text(["version 1.0", "game by killpassed"])

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        save_settings(self.game.settings)
                        return
                    elif e.key == pygame.K_UP:
                        selected = (selected - 1) % len(items)
                    elif e.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(items)
                    elif e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.change_setting(items[selected])
                        save_settings(self.game.settings)

    def change_setting(self, key):
        if key == "language":
            self.game.settings["language"] = "en" if self.game.settings["language"] == "ru" else "ru"
        elif key == "controls":
            self.game.settings["controls"] = "wasd" if self.game.settings["controls"] == "arrows" else "arrows"
        elif key == "color":
            self.game.settings["snake_color"] = (self.game.settings["snake_color"] + 1) % len(SNAKE_COLORS)
            self.game.snake_color = SNAKE_COLORS[self.game.settings["snake_color"]]
        elif key == "resolution":
            self.game.settings["resolution"] = (self.game.settings["resolution"] + 1) % len(RESOLUTIONS)
            self.game.apply_resolution()
        elif key == "grid":
            self.game.settings["show_grid"] = not self.game.settings["show_grid"]
        elif key == "fullscreen":
            self.game.settings["fullscreen"] = not self.game.settings["fullscreen"]
            self.game.apply_resolution()
