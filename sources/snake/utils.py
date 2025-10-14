import json, os
from pathlib import Path

APPDATA_PATH = Path(os.getenv("APPDATA")) / "Local" / "vkmontedd-games" / "Snake"
SETTINGS_FILE = APPDATA_PATH / "settings.json"

DEFAULT_SETTINGS = {
    "language": "ru",
    "controls": "arrows",
    "snake_color": 0,
    "resolution": 0,
    "show_grid": False,
    "fullscreen": False,
    "high_score": 0
}

def ensure_settings_complete(data):
    for k, v in DEFAULT_SETTINGS.items():
        if k not in data:
            data[k] = v
    return data

def load_settings():
    APPDATA_PATH.mkdir(parents=True, exist_ok=True)
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = DEFAULT_SETTINGS.copy()
    else:
        data = DEFAULT_SETTINGS.copy()
    data = ensure_settings_complete(data)
    save_settings(data)
    return data

def save_settings(data):
    APPDATA_PATH.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(ensure_settings_complete(data), f, indent=4, ensure_ascii=False)
