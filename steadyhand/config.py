from enum import Enum

# --- 螢幕設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- 遊戲狀態 (使用 Enum 更清晰) ---
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    LEVEL_CLEAR = 2
    GAME_OVER = 3
    GAME_WIN = 4

# --- 顏色 (R, G, B) ---
COLOR_BACKGROUND = (20, 20, 40)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_TEXT_WIN = (0, 255, 0)
COLOR_TEXT_LOSE = (255, 0, 0)

COLOR_PLAYER = (255, 50, 50)
COLOR_WALL = (100, 100, 120)
COLOR_GOAL = (50, 255, 50)

# --- 資源路徑 ---
FONT_PATH = "assets/fonts/Roboto-Regular.ttf"

# --- 遊戲設定 ---
PLAYER_SIZE = 10