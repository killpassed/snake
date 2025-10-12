import pygame
from snake.strings import STRINGS
from snake.config import SNAKE_COLORS, RESOLUTIONS
from snake.utils import save_settings
from snake.config import CONTROL_SETS

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
        while True:
            lang = self.game.settings.get("language", "ru")
            s = STRINGS.get(lang, STRINGS["ru"])
            options = [s["play"], s["settings"], s["quit"]]

            self.game.screen.fill((0, 0, 0))
            self.draw_text(s["title"], 72, self.game.height // 4, self.game.snake_color)

            for i, opt in enumerate(options):
                color = (255, 255, 255) if i == self.selected else (150, 150, 150)
                self.draw_text(opt, 40, self.game.height // 2 + i * 60, color)

            self.draw_corner_text(["version 1.1", "game by killpassed"])

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
        items = ["language", "controls", "color", "resolution", "grid", "fullscreen", "back"]
        selected = 0

        while True:
            lang = self.game.settings.get("language", "ru")
            s = STRINGS.get(lang, STRINGS["ru"])
            self.game.screen.fill((0, 0, 0))

            for i, key in enumerate(items):
                text = s.get(key, key)
                if key == "language":
                    val = "Русский" if self.game.settings.get("language", "ru") == "ru" else "English"
                elif key == "controls":
                    val = "WASD" if self.game.settings.get("controls", "arrows") == "wasd" else "↑↓←→"
                elif key == "color":
                    val = str(self.game.settings.get("snake_color", 0) + 1)
                elif key == "resolution":
                    res = RESOLUTIONS[self.game.settings.get("resolution", 0)]
                    val = f"{res[0]}x{res[1]}"
                elif key == "grid":
                    val = s["on"] if self.game.settings.get("show_grid", False) else s["off"]
                elif key == "fullscreen":
                    val = s["on"] if self.game.settings.get("fullscreen", False) else s["off"]
                elif key == "back":
                    val = ""
                txt = f"{text}: {val}" if val != "" else text
                color = (255, 255, 255) if i == selected else (120, 120, 120)
                self.draw_text(txt, 36, self.game.height // 3 + i * 60, color)

            self.draw_corner_text(["version 1.1", "game by killpassed"])
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    save_settings(self.game.settings)
                    return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        save_settings(self.game.settings)
                        return
                    elif e.key == pygame.K_UP:
                        selected = (selected - 1) % len(items)
                    elif e.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(items)
                    elif e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
                        key = items[selected]
                        self.change_setting(key)
                        save_settings(self.game.settings)

    def change_setting(self, key):
        if key == "language":
            self.game.settings["language"] = "en" if self.game.settings.get("language", "ru") == "ru" else "ru"
        elif key == "controls":
            self.game.settings["controls"] = "wasd" if self.game.settings.get("controls", "arrows") == "arrows" else "arrows"
            self.game.controls = CONTROL_SETS[self.game.settings["controls"]]
        elif key == "color":
            idx = (self.game.settings.get("snake_color", 0) + 1) % len(SNAKE_COLORS)
            self.game.settings["snake_color"] = idx
            self.game.snake_color = SNAKE_COLORS[idx]
            if hasattr(self.game, "snake") and self.game.snake:
                self.game.snake.color = SNAKE_COLORS[idx]
        elif key == "resolution":
            idx = (self.game.settings.get("resolution", 0) + 1) % len(RESOLUTIONS)
            self.game.settings["resolution"] = idx
            self.game.apply_resolution()
        elif key == "grid":
            self.game.settings["show_grid"] = not self.game.settings.get("show_grid", False)
        elif key == "fullscreen":
            self.game.settings["fullscreen"] = not self.game.settings.get("fullscreen", False)
            self.game.apply_resolution()
        elif key == "back":
            save_settings(self.game.settings)
