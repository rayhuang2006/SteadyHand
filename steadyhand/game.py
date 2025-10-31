import cpygfx
from .config import (
    GameState, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH,
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_TEXT_DIM, 
    COLOR_TEXT_WIN, COLOR_TEXT_LOSE
)
from .entities import Player
from .level_manager import LevelManager
from .utils import check_collision

class Game:
    """
    遊戲主類別，包含主迴圈、狀態機和所有遊戲邏輯。
    """
    def __init__(self):
        self.level_manager = LevelManager("levels")
        self.state = GameState.MENU
        
        self.player = Player(0, 0, 10)
        self.walls = []
        self.goal = None
        self.current_level_index = 0
        
        # 載入字型 (我們在 V2 中只需要載入一次)
        if not cpygfx.load_font(FONT_PATH, 32):
             print(f"警告：載入字型 {FONT_PATH} (32pt) 失敗")
        
        print("遊戲物件初始化完成。")

    def load_level(self, level_index: int):
        """ 載入一個新關卡並設定遊戲狀態 """
        
        # --- (修正邏輯 1) ---
        # 我們將 "勝利" 檢查移到 update 函式中，
        # 這裡只專注於載入。
        # (原有的 'if level_index >= ...' 檢查已被移除)
        
        level_data = self.level_manager.load_level_data(level_index)
        
        if level_data is None:
            # 這現在只會處理「真正的」載入失敗 (例如 JSON 格式錯誤)
            print(f"關卡 {level_index} 載入失敗，回到選單。")
            self.state = GameState.MENU
            return

        self.walls = level_data["walls"]
        self.goal = level_data["goal"]
        self.player.set_pos(level_data["start_pos"][0], level_data["start_pos"][1])
        self.current_level_index = level_index
        self.state = GameState.PLAYING

    def run(self):
        """ 遊戲主迴圈 """
        print("開始遊戲主迴圈...")
        running = True
        while running:
            # 1. 處理輸入
            if cpygfx.poll_event():
                running = False
                
            mouse_x = cpygfx.get_mouse_x()
            mouse_y = cpygfx.get_mouse_y()
            clicked = cpygfx.get_mouse_clicked()
            
            # 2. 更新遊戲狀態 (狀態機)
            self.update(mouse_x, mouse_y, clicked)
            
            # 3. 渲染
            self.render()
            
            # 4. 更新螢幕
            cpygfx.update()
            
    def update(self, mouse_x, mouse_y, clicked):
        """ 根據遊戲狀態更新邏輯 """
        
        if self.state == GameState.PLAYING:
            self.player.set_pos(mouse_x, mouse_y)
            player_rect = self.player.rect
            
            # 檢查是否撞牆
            for wall in self.walls:
                if check_collision(player_rect, wall.rect):
                    self.state = GameState.GAME_OVER
                    return 
            
            # 檢查是否到終點
            if self.goal and check_collision(player_rect, self.goal.rect):
                self.state = GameState.LEVEL_CLEAR
                return

        elif self.state == GameState.MENU:
            if clicked:
                self.load_level(0) # 開始第一關

        elif self.state == GameState.GAME_OVER:
            if clicked:
                # 重新載入目前關卡
                self.load_level(self.current_level_index)

        elif self.state == GameState.LEVEL_CLEAR:
            if clicked:
                # --- (核心修正邏輯) ---
                # 先計算下一個關卡索引
                next_index = self.current_level_index + 1
                
                # 檢查是否還有下一關
                if next_index >= self.level_manager.get_level_count():
                    # 沒有了 -> 勝利！
                    self.state = GameState.GAME_WIN
                else:
                    # 還有 -> 載入下一關
                    self.load_level(next_index)
                # --- (修正結束) ---
                
        elif self.state == GameState.GAME_WIN:
            if clicked:
                # 回到選單
                self.state = GameState.MENU

    def render(self):
        """ 根據遊戲狀態渲染畫面 """
        
        # 1. 清除背景
        c = COLOR_BACKGROUND
        cpygfx.clear(c[0], c[1], c[2])
        
        # 2. 根據狀態繪製
        if self.state == GameState.MENU:
            c = COLOR_TEXT
            cpygfx.draw_text("Steady Hand Game (V2)", 200, 250, c[0], c[1], c[2])
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Click to Start", 300, 300, c[0], c[1], c[2])

        elif self.state == GameState.PLAYING:
            self.render_level()

        elif self.state == GameState.GAME_OVER:
            self.render_level() 
            c = COLOR_TEXT_LOSE
            cpygfx.draw_text("GAME OVER", 300, 250, c[0], c[1], c[2])
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Click to Retry", 300, 300, c[0], c[1], c[2])

        elif self.state == GameState.LEVEL_CLEAR:
            self.render_level() 
            c = COLOR_TEXT_WIN
            cpygfx.draw_text("Level Clear!", 300, 250, c[0], c[1], c[2])
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Click to Continue", 280, 300, c[0], c[1], c[2])
            
        elif self.state == GameState.GAME_WIN:
            c = COLOR_TEXT_WIN
            cpygfx.draw_text("YOU WIN!", 320, 250, c[0], c[1], c[2])
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Click to Return to Menu", 250, 300, c[0], c[1], c[2])

    def render_level(self):
        """ 繪製所有關卡物件 """
        for wall in self.walls:
            wall.draw()
        if self.goal:
            self.goal.draw()
        self.player.draw()