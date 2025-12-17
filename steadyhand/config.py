# 檔案名稱: steadyhand/config.py
from .themes import THEMES
from .utils import load_env_file

# [新增] 載入環境變數
_env = load_env_file(".env")
UI_STYLE = (_env.get("UI_STYLE", "classic") or "classic").strip().lower()

# [新增] 伺服器設定 (優先讀取 .env，讀不到則使用預設值)
SERVER_HOST = _env.get("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(_env.get("SERVER_PORT", "9999"))

# --- 視窗設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

_theme = THEMES.get(UI_STYLE, THEMES["classic"])

# --- 現代幾何配色 ---
COLOR_BG = _theme["COLOR_BG"]
COLOR_GRID = _theme["COLOR_GRID"]

# 實體顏色
COLOR_WALL_BODY = _theme["COLOR_WALL_BODY"]
COLOR_WALL_BORDER = _theme["COLOR_WALL_BORDER"]
COLOR_WALL_SHADOW = _theme["COLOR_WALL_SHADOW"]
COLOR_PLAYER_CORE = _theme["COLOR_PLAYER_CORE"]
COLOR_PLAYER_TRAIL = _theme["COLOR_PLAYER_TRAIL"]
COLOR_GOAL = _theme["COLOR_GOAL"]

# UI 互動配色
COLOR_UI_NORMAL = _theme["COLOR_UI_NORMAL"]
COLOR_UI_HOVER = _theme["COLOR_UI_HOVER"]
COLOR_UI_BORDER_HOVER = _theme["COLOR_UI_BORDER_HOVER"]
COLOR_UI_LOCKED_BG = _theme["COLOR_UI_LOCKED_BG"]
COLOR_UI_LOCKED_FG = _theme["COLOR_UI_LOCKED_FG"]

# 特效配色
COLOR_TRANSITION = _theme["COLOR_TRANSITION"]
COLOR_PAUSE_BG = _theme["COLOR_PAUSE_BG"]
COLOR_PARTICLE_SPARK = _theme["COLOR_PARTICLE_SPARK"]
COLOR_PARTICLE_TRAIL = _theme["COLOR_PARTICLE_TRAIL"]
COLOR_STAR_ON = _theme["COLOR_STAR_ON"]
COLOR_STAR_OFF = _theme["COLOR_STAR_OFF"]

# UI metrics
UI_TITLE_SIZE = _theme.get("UI_TITLE_SIZE", 56)
UI_TEXT_SIZE  = _theme.get("UI_TEXT_SIZE", 24)
UI_LINE_W     = _theme.get("UI_LINE_W", 2)
UI_PANEL_FILL = _theme.get("UI_PANEL_FILL", (15, 20, 30))
UI_BTN_FILL   = _theme.get("UI_BTN_FILL", (30, 35, 50))
UI_BTN_FILL_HOVER = _theme.get("UI_BTN_FILL_HOVER", UI_BTN_FILL)
UI_GLOW = _theme.get("UI_GLOW", {"enabled": False})

# --- 語言 ---
LANGUAGE = _env.get("LANGUAGE", "en")

# --- 資源 ---
FONT_PATH = _theme["FONT_PATH"]
if LANGUAGE == "zh": 
    FONT_PATH = _theme["FONT_PATH_TW"]

# --- 遊戲參數 ---
PLAYER_SIZE = 14
PLAYER_ACCEL = 0.8
PLAYER_FRICTION = 0.90
PLAYER_MAX_SPEED = 5.0
STAR_3_TIME = 15.0
STAR_2_TIME = 30.0

# --- debug ---
def dump_config():
    configs = {
        "UI_STYLE": UI_STYLE,
        "LANGUAGE": LANGUAGE,
        "FONT_PATH": FONT_PATH,
    }

    for key, value in configs.items():
        print(f"{key}: {value}")

dump_config()
