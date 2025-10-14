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

    def draw_background(self):
        self.game.screen.fill((0, 0, 0))

    def run(self):
        pygame.mouse.set_visible(False)
        while True:
            s = STRINGS[self.game.settings["language"]]
            options = [s["play"], s["high_scores"], s["settings"], s["quit"]]

            self.draw_background()
            self.draw_text(s["title"], 72, self.game.height // 4, self.game.snake_color)
            for i, opt in enumerate(options):
                color = (255, 255, 255) if i == self.selected else (150, 150, 150)
                self.draw_text(opt, 40, self.game.height // 2 + i * 60, color)
            self.draw_corner_text(["version 1.2", "game by vkmontedd"])
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(options)
                    elif e.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(options)
                    elif e.key in (pygame.K_RETURN, pygame.K_LEFT, pygame.K_RIGHT):
                        if self.selected == 0:
                            return "play"
                        elif self.selected == 1:
                            self.high_scores_menu()
                        elif self.selected == 2:
                            self.settings_menu()
                        elif self.selected == 3:
                            return "quit"

    def settings_menu(self):
        selected = 0
        while True:
            s = STRINGS[self.game.settings["language"]]
            items = ["language", "controls", "color", "resolution", "grid", "fullscreen", "back"]

            self.draw_background()
            for i, key in enumerate(items):
                if key == "back":
                    text = s["back"]
                    val = ""
                else:
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
                txt = f"{text}: {val}" if val else text
                color = (255, 255, 255) if i == selected else (120, 120, 120)
                self.draw_text(txt, 36, self.game.height // 3 + i * 60, color)

            self.draw_corner_text(["version 1.2", "game by vkmontedd"])
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
                    elif e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
                        if items[selected] == "back":
                            save_settings(self.game.settings)
                            return
                        else:
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

    def high_scores_menu(self):
        s = STRINGS[self.game.settings["language"]]
        while True:
            self.draw_background()
            font_big = pygame.font.SysFont("arial", 60, True)
            font_small = pygame.font.SysFont("arial", 36)
            title = font_big.render(s["high_scores"], True, (255, 255, 255))
            self.game.screen.blit(title, (self.game.width // 2 - title.get_width() // 2, self.game.height // 4))

            score_text = font_small.render(f"{s['record']}: {self.game.settings.get('highscore', 0)}", True, (255, 255, 255))
            self.game.screen.blit(score_text, (self.game.width // 2 - score_text.get_width() // 2, self.game.height // 2))

            hint = font_small.render(s["press_enter"], True, (150, 150, 150))
            self.game.screen.blit(hint, (self.game.width // 2 - hint.get_width() // 2, self.game.height - 80))
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return
                elif e.type == pygame.QUIT:
                    return
