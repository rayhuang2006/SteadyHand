# 檔案名稱: steadyhand/entities.py
import cpygfx
import math
# 明確匯入按鍵，避免錯誤
from cpygfx.keys import KEY_W, KEY_A, KEY_S, KEY_D, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from .config import *
from .utils import Rect

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.size = PLAYER_SIZE
        # 幾何風格不需要 image，但為了相容舊介面保留參數
        self.rect = Rect(x, y, self.size, self.size)
        
        # [視覺特效] 拖尾紀錄
        # 儲存格式: (x, y, size)
        self.trail = [] 

    def set_pos(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.trail.clear() # 重置位置時清空拖尾
        self.update_rect()

    def update(self):
        # 1. 更新拖尾 (每幀記錄一次位置)
        # 為了效能和視覺，我們只保留最近 8 個點
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 8:
            self.trail.pop(0)

        # 2. 物理輸入處理
        if cpygfx.is_key_down(KEY_W) or cpygfx.is_key_down(KEY_UP): self.vy -= PLAYER_ACCEL
        if cpygfx.is_key_down(KEY_S) or cpygfx.is_key_down(KEY_DOWN): self.vy += PLAYER_ACCEL
        if cpygfx.is_key_down(KEY_A) or cpygfx.is_key_down(KEY_LEFT): self.vx -= PLAYER_ACCEL
        if cpygfx.is_key_down(KEY_D) or cpygfx.is_key_down(KEY_RIGHT): self.vx += PLAYER_ACCEL
        
        # 摩擦力
        self.vx *= PLAYER_FRICTION
        self.vy *= PLAYER_FRICTION
        
        # 速度限制
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > PLAYER_MAX_SPEED:
            scale = PLAYER_MAX_SPEED / speed
            self.vx *= scale
            self.vy *= scale
            
        # 更新座標
        self.x += self.vx
        self.y += self.vy
        
        # 邊界檢查
        if self.x < 0: self.x = 0; self.vx = 0
        elif self.x > SCREEN_WIDTH - self.size: self.x = SCREEN_WIDTH - self.size; self.vx = 0
        if self.y < 0: self.y = 0; self.vy = 0
        elif self.y > SCREEN_HEIGHT - self.size: self.y = SCREEN_HEIGHT - self.size; self.vy = 0
        
        self.update_rect()

    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        # 1. 繪製拖尾 (粒子感)
        # 我們讓拖尾從小變大，且透明度(這裡模擬為亮度)越來越高
        tc = COLOR_PLAYER_TRAIL
        cx = self.size // 2
        cy = self.size // 2
        
        for i, pos in enumerate(self.trail):
            # 拖尾大小隨索引變化 (0是最舊的，7是最新的)
            t_size = 4 + i  
            # 亮度/顏色模擬 (越新的越亮)
            brightness = 50 + i * 25
            
            # 畫在中心
            tx = pos[0] + cx - t_size // 2
            ty = pos[1] + cy - t_size // 2
            
            # 畫實心方塊模擬粒子
            cpygfx.draw_rect_filled(tx, ty, t_size, t_size, 0, brightness, brightness)

        # 2. 繪製核心 (Player Core)
        x, y, s = self.rect.x, self.rect.y, self.size
        
        # 外發光框 (青色)
        c = COLOR_PLAYER_CORE
        cpygfx.draw_rect(x, y, s, s, c[0], c[1], c[2])
        
        # 實心核心 (高亮白青色)
        padding = 3
        cpygfx.draw_rect_filled(x+padding, y+padding, s-padding*2, s-padding*2, 200, 255, 255)

class Wall:
    def __init__(self, x, y, width, height, move_axis=None, move_dist=0, move_speed=0, **kwargs):
        self.rect = Rect(x, y, width, height)
        
        # 記錄初始位置
        self.start_x = x
        self.start_y = y
        
        # 接收移動參數 (如果有傳入的話)
        self.move_axis = move_axis
        self.move_dist = move_dist
        self.move_speed = move_speed

    def update(self):
        # 恢復移動邏輯
        if self.move_axis:
            # 取得時間 (秒)
            t = cpygfx.get_ticks() / 1000.0
            # 計算 Sin 波位移
            offset = math.sin(t * self.move_speed) * self.move_dist
            
            if self.move_axis == 'x':
                self.rect.x = int(self.start_x + offset)
            elif self.move_axis == 'y':
                self.rect.y = int(self.start_y + offset)

    def draw(self):
        x, y, w, h = self.rect.x, self.rect.y, self.rect.w, self.rect.h
        
        # 1. 陰影 (Shadow)
        sc = COLOR_WALL_SHADOW
        cpygfx.draw_rect_filled(x+6, y+6, w, h, sc[0], sc[1], sc[2])
        
        # 2. 本體 (Body)
        bc = COLOR_WALL_BODY
        cpygfx.draw_rect_filled(x, y, w, h, bc[0], bc[1], bc[2])
        
        # 3. 邊框 (Border)
        lc = COLOR_WALL_BORDER
        cpygfx.draw_rect(x, y, w, h, lc[0], lc[1], lc[2])

class Goal:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def draw(self):
        x, y, w, h = self.rect.x, self.rect.y, self.rect.w, self.rect.h
        c = COLOR_GOAL
        
        # 呼吸燈效果
        ticks = cpygfx.get_ticks()
        pulse = int(math.sin(ticks / 150.0) * 80 + 175) # 亮度在 95~255 之間跳動
        
        # 外框
        cpygfx.draw_rect(x, y, w, h, 0, pulse, 0)
        
        # 內部縮小的實心塊
        gap = 6
        cpygfx.draw_rect_filled(x+gap, y+gap, w-gap*2, h-gap*2, 0, pulse, 0)