# 檔案名稱: steadyhand/game.py
import cpygfx
from cpygfx.keys import KEY_ENTER # 我們用 ENTER 鍵來確認選單
from .config import (
    GameState, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH,
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_TEXT_DIM, 
    COLOR_TEXT_WIN, COLOR_TEXT_LOSE
)
from .entities import Player
from .level_manager import LevelManager
from .utils import check_collision

class Game:
    def __init__(self):
        self.level_manager = LevelManager("levels")
        self.state = GameState.MENU
        
        # 玩家初始位置會由 load_level 覆蓋
        self.player = Player(0, 0, 16) 
        self.walls = []
        self.goal = None
        self.current_level_index = 0
        
        if not cpygfx.load_font(FONT_PATH, 32):
             print(f"警告：載入字型 {FONT_PATH}失敗")
        print("遊戲物件初始化完成。")

    def load_level(self, level_index: int):
        level_data = self.level_manager.load_level_data(level_index)
        
        if level_data is None:
            print(f"關卡 {level_index} 載入失敗，回到選單。")
            self.state = GameState.MENU
            return

        self.walls = level_data["walls"]
        self.goal = level_data["goal"]
        # 設定玩家起始位置 (同時會重置速度為 0)
        self.player.set_pos(level_data["start_pos"][0], level_data["start_pos"][1])
        self.current_level_index = level_index
        self.state = GameState.PLAYING

    def run(self):
        print("開始遊戲主迴圈 (WASD 控制版)...")
        running = True
        while running:
            # FPS 鎖定
            cpygfx.delay(16) 

            # 1. 處理系統事件 (如關閉視窗)
            if cpygfx.poll_event():
                running = False
            
            # 我們不再需要每幀讀取滑鼠，改在 update 裡讀鍵盤
            
            # 2. 更新遊戲邏輯
            self.update()
            
            # 3. 渲染
            self.render()
            
            # 4. 更新螢幕
            cpygfx.update()
            
    def update(self):
        """ 根據遊戲狀態更新邏輯 """
        
        # 取得一些通用輸入
        clicked = cpygfx.get_mouse_clicked()
        enter_pressed = cpygfx.is_key_down(KEY_ENTER) # 支援鍵盤確認
        
        if self.state == GameState.PLAYING:
            # --- [核心修改] 玩家物理更新 ---
            self.player.update()
            # ---------------------------
            
            # 牆壁移動
            for wall in self.walls:
                wall.update()
            
            player_rect = self.player.rect
            
            # 撞牆檢查
            for wall in self.walls:
                if check_collision(player_rect, wall.rect):
                    self.state = GameState.GAME_OVER
                    return 
            
            # 終點檢查
            if self.goal and check_collision(player_rect, self.goal.rect):
                self.state = GameState.LEVEL_CLEAR
                return

        elif self.state == GameState.MENU:
            if clicked or enter_pressed:
                self.load_level(0) 

        elif self.state == GameState.GAME_OVER:
            if clicked or enter_pressed:
                self.load_level(self.current_level_index)

        elif self.state == GameState.LEVEL_CLEAR:
            if clicked or enter_pressed:
                next_index = self.current_level_index + 1
                if next_index >= self.level_manager.get_level_count():
                    self.state = GameState.GAME_WIN
                else:
                    self.load_level(next_index)
                # 簡單的防彈跳 (Debounce)，避免 ENTER 一次跳兩關
                # 這裡只是暫時解法，正式專案通常會有 InputManager 處理 KeyUp
                cpygfx.delay(200) 
                
        elif self.state == GameState.GAME_WIN:
            if clicked or enter_pressed:
                self.state = GameState.MENU
                cpygfx.delay(200)

    def render(self):
        # (渲染邏輯保持不變，會直接畫出更新後的玩家位置)
        c = COLOR_BACKGROUND
        cpygfx.clear(c[0], c[1], c[2])
        
        if self.state == GameState.MENU:
            c = COLOR_TEXT
            cpygfx.draw_text("Cyber Circuit", 200, 200, 0, 255, 255) # 改標題
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("WASD to Move / ENTER to Start", 180, 300, c[0], c[1], c[2])

        elif self.state == GameState.PLAYING:
            self.render_level()

        elif self.state == GameState.GAME_OVER:
            self.render_level() 
            c = COLOR_TEXT_LOSE
            cpygfx.draw_text("CIRCUIT BROKEN", 250, 250, c[0], c[1], c[2]) # 改文字
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Press ENTER to Retry", 250, 300, c[0], c[1], c[2])

        elif self.state == GameState.LEVEL_CLEAR:
            self.render_level() 
            c = COLOR_TEXT_WIN
            cpygfx.draw_text("SYNC COMPLETE", 250, 250, c[0], c[1], c[2]) # 改文字
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Press ENTER for Next Node", 200, 300, c[0], c[1], c[2])
            
        elif self.state == GameState.GAME_WIN:
            c = COLOR_TEXT_WIN
            cpygfx.draw_text("SYSTEM RESTORED", 250, 250, c[0], c[1], c[2])
            c = COLOR_TEXT_DIM
            cpygfx.draw_text("Press ENTER to Reboot", 220, 300, c[0], c[1], c[2])

    def render_level(self):
        for wall in self.walls:
            wall.draw()
        if self.goal:
            self.goal.draw()
        self.player.draw()