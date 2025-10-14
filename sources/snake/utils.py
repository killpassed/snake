import json
import os
from pathlib import Path

def get_settings_path():
    base_dir = Path(os.getenv("LOCALAPPDATA", Path.home()))
    settings_dir = base_dir / "killpassed-games" / "Snake"
    settings_dir.mkdir(parents=True, exist_ok=True)
    return settings_dir / "settings.json"

SETTINGS_PATH = get_settings_path()

DEFAULT_SETTINGS = {
    "language": "ru",
    "controls": "arrows",
    "color": 0,
    "resolution": 0,
    "grid": False,
    "fullscreen": False
}

def load_settings():
    try:
        if SETTINGS_PATH.exists():
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                settings = json.load(f)
            updated = False
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
                    updated = True
            if updated:
                save_settings(settings)
            return settings
        else:
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")

def get_data_dir():
    return SETTINGS_PATH.parent

def get_highscores_path():
    return get_data_dir() / "highscores.json"

def load_highscores():
    path = get_highscores_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения рекордов: {e}")
        return []

def save_highscore(score):
    path = get_highscores_path()
    try:
        scores = load_highscores()
        scores.append(score)
        scores = sorted(scores, reverse=True)[:10]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения рекордов: {e}")
