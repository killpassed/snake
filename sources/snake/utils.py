import json
import os

def load_settings():
    if not os.path.exists("settings.json"):
        return {
            "language": "ru",
            "controls": "arrows",
            "snake_color": 0,
            "resolution": 0,
            "show_grid": False,
            "fullscreen": False
        }
    with open("settings.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
