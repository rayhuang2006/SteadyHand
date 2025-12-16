# 檔案名稱: steadyhand/config.py
from .utils import load_env_file

# [新增] 載入環境變數
_env = load_env_file(".env")

# [新增] 伺服器設定 (優先讀取 .env，讀不到則使用預設值)
SERVER_HOST = _env.get("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(_env.get("SERVER_PORT", "9999"))

# --- 視窗設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- 現代幾何配色 ---
COLOR_BG = (10, 12, 20) 
COLOR_GRID = (30, 35, 50)

# 實體顏色
COLOR_WALL_BODY = (40, 45, 60)
COLOR_WALL_BORDER = (200, 220, 255)
COLOR_WALL_SHADOW = (5, 5, 10)
COLOR_PLAYER_CORE = (0, 255, 255)
COLOR_PLAYER_TRAIL = (0, 100, 100)
COLOR_GOAL = (50, 255, 100)

# UI 互動配色
COLOR_UI_NORMAL = (150, 160, 180)
COLOR_UI_HOVER = (0, 255, 255)
COLOR_UI_BORDER_HOVER = (100, 255, 255)
COLOR_UI_LOCKED_BG = (20, 25, 35)
COLOR_UI_LOCKED_FG = (60, 70, 90)

# 特效配色
COLOR_TRANSITION = (15, 20, 30)
COLOR_PAUSE_BG = (0, 0, 0)
COLOR_PARTICLE_SPARK = (255, 255, 100)
COLOR_PARTICLE_TRAIL = (0, 200, 255)
COLOR_STAR_ON = (255, 215, 0)
COLOR_STAR_OFF = (60, 60, 80)

# --- 資源 ---
FONT_PATH = "assets/fonts/NotoSansTC-Regular.ttf"

# --- 語言 ---
DEFAULT_LANG = "en" # en | zh

# --- 遊戲參數 ---
PLAYER_SIZE = 14
PLAYER_ACCEL = 0.8
PLAYER_FRICTION = 0.90
PLAYER_MAX_SPEED = 5.0
STAR_3_TIME = 15.0
STAR_2_TIME = 30.0
