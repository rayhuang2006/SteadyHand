# steadyhand/themes.py
# ------------------------------------------------------------
# UI Themes definition
# ------------------------------------------------------------

THEMES = {
    "classic": {
        "NAME": "Classic",

        "BG_PATH": "",
        "COLOR_BG": (10, 12, 20),
        "COLOR_GRID": (30, 35, 50),

        "COLOR_WALL_BODY": (40, 45, 60),
        "COLOR_WALL_BORDER": (200, 220, 255),
        "COLOR_WALL_SHADOW": (5, 5, 10),

        "COLOR_PLAYER_CORE": (0, 255, 255),
        "COLOR_PLAYER_TRAIL": (0, 100, 100),
        "COLOR_GOAL": (50, 255, 100),

        "COLOR_UI_NORMAL": (150, 160, 180),
        "COLOR_UI_HOVER": (0, 255, 255),
        "COLOR_UI_BORDER_HOVER": (100, 255, 255),
        "COLOR_UI_LOCKED_BG": (20, 25, 35),
        "COLOR_UI_LOCKED_FG": (60, 70, 90),

        "COLOR_TRANSITION": (15, 20, 30),
        "COLOR_PAUSE_BG": (0, 0, 0),

        "COLOR_PARTICLE_SPARK": (255, 255, 100),
        "COLOR_PARTICLE_TRAIL": (0, 200, 255),

        "COLOR_STAR_ON": (255, 215, 0),
        "COLOR_STAR_OFF": (60, 60, 80),

        "FONT_PATH": "assets/fonts/ShareTechMono-Regular.ttf",
        "FONT_PATH_TW": "assets/fonts/NotoSansTC-Regular.ttf",

        # UI metrics
        "UI_TITLE_SIZE": 56,
        "UI_TEXT_SIZE": 24,
        "UI_LINE_W": 2,
        "UI_PANEL_FILL": (15, 20, 30),
        "UI_BTN_FILL": (30, 35, 50),
        "UI_BTN_FILL_HOVER": (35, 45, 65),

        "UI_GLOW": {
            "enabled": False
        }
    },

    # --------------------------------------------------------
    # TRON / 創：戰神 風格
    # --------------------------------------------------------
    "tron": {
        "NAME": "TRON Legacy",

        "BG_PATH": "assets/images/bg_red.png",
        "COLOR_BG": (3, 6, 12),
        "COLOR_GRID": (0, 28, 40),

        "COLOR_WALL_BODY": (7, 14, 26),
        "COLOR_WALL_BORDER": (0, 230, 255),
        "COLOR_WALL_SHADOW": (0, 0, 0),

        "COLOR_PLAYER_CORE": (0, 240, 255),
        "COLOR_PLAYER_TRAIL": (0, 120, 140),
        "COLOR_GOAL": (120, 255, 190),

        "COLOR_UI_NORMAL": (120, 190, 200),
        "COLOR_UI_HOVER": (0, 230, 255),
        "COLOR_UI_BORDER_HOVER": (160, 255, 255),
        "COLOR_UI_LOCKED_BG": (8, 12, 20),
        "COLOR_UI_LOCKED_FG": (35, 70, 80),

        "COLOR_TRANSITION": (0, 20, 28),
        "COLOR_PAUSE_BG": (0, 0, 0),

        "COLOR_PARTICLE_SPARK": (255, 255, 160),
        "COLOR_PARTICLE_TRAIL": (0, 230, 255),

        "COLOR_STAR_ON": (0, 230, 255),
        "COLOR_STAR_OFF": (20, 50, 60),

        "FONT_PATH": "assets/fonts/ShareTechMono-Regular.ttf",
        "FONT_PATH_TW": "assets/fonts/LXGWWenKaiMonoTC-Regular.ttf",

        # UI metrics
        "UI_TITLE_SIZE": 60,
        "UI_TEXT_SIZE": 24,
        "UI_LINE_W": 2,
        "UI_PANEL_FILL": (6, 10, 18),
        "UI_BTN_FILL": (6, 12, 24),
        "UI_BTN_FILL_HOVER": (8, 18, 28),

        "UI_GLOW": {
            "enabled": True,
            "passes": 3,
            "spread": 2
        }
    },

    # --------------------------------------------------------
    # TRON 霓虹紅
    # --------------------------------------------------------
    "tron_red": {
        "NAME": "TRON Neon Red",

        "BG_PATH": "assets/images/bg_blue.png",
        "COLOR_BG": (6, 2, 8),                 # 更偏紫黑的深底，紅光更亮
        "COLOR_GRID": (40, 0, 18),

        "COLOR_WALL_BODY": (14, 6, 14),
        "COLOR_WALL_BORDER": (255, 40, 120),   # 霓虹紅（偏桃紅）
        "COLOR_WALL_SHADOW": (0, 0, 0),

        "COLOR_PLAYER_CORE": (255, 70, 150),
        "COLOR_PLAYER_TRAIL": (120, 20, 70),
        "COLOR_GOAL": (255, 140, 80),          # 終點改成暖橘紅，跟邊框分得開

        "COLOR_UI_NORMAL": (200, 120, 160),
        "COLOR_UI_HOVER": (255, 40, 120),
        "COLOR_UI_BORDER_HOVER": (255, 180, 220),
        "COLOR_UI_LOCKED_BG": (10, 6, 14),
        "COLOR_UI_LOCKED_FG": (90, 40, 70),

        "COLOR_TRANSITION": (20, 0, 18),
        "COLOR_PAUSE_BG": (0, 0, 0),

        "COLOR_PARTICLE_SPARK": (255, 220, 200),
        "COLOR_PARTICLE_TRAIL": (255, 40, 120),

        "COLOR_STAR_ON": (255, 40, 120),
        "COLOR_STAR_OFF": (40, 10, 25),

        "FONT_PATH": "assets/fonts/ShareTechMono-Regular.ttf",
        "FONT_PATH_TW": "assets/fonts/LXGWWenKaiMonoTC-Regular.ttf",

        "UI_TITLE_SIZE": 60,
        "UI_TEXT_SIZE": 24,
        "UI_LINE_W": 2,
        "UI_PANEL_FILL": (10, 6, 14),
        "UI_BTN_FILL": (16, 8, 20),
        "UI_BTN_FILL_HOVER": (18, 10, 26),

        "UI_GLOW": {
            "enabled": True,
            "passes": 3,
            "spread": 2
        }
    },
}
