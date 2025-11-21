import math
import cpygfx
from cpygfx.keys import KEY_W, KEY_A, KEY_S, KEY_D, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from .config import (
    COLOR_PLAYER, COLOR_WALL, COLOR_GOAL, 
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_ACCEL, PLAYER_FRICTION, PLAYER_MAX_SPEED
)
from .utils import Rect

class Player:
    def __init__(self, x: int, y: int, size: int):
        self.size = size
        # 使用浮點數來記錄精確位置，這樣物理計算才會平滑
        self.x = float(x)
        self.y = float(y)
        
        # 速度向量 (Velocity)
        self.vx = 0.0
        self.vy = 0.0
        
        # 碰撞判定框 (整數)
        self.rect = Rect(x, y, size, size)

    def set_pos(self, x: int, y: int):
        """ 強制設定位置 (用於重置關卡) """
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.update_rect()

    def update(self):
        """ 每一幀呼叫一次，計算物理移動 """
        
        # 1. 偵測輸入並施加加速度
        # 支援 WASD 和 方向鍵
        if cpygfx.is_key_down(KEY_W) or cpygfx.is_key_down(KEY_UP):
            self.vy -= PLAYER_ACCEL
        if cpygfx.is_key_down(KEY_S) or cpygfx.is_key_down(KEY_DOWN):
            self.vy += PLAYER_ACCEL
        if cpygfx.is_key_down(KEY_A) or cpygfx.is_key_down(KEY_LEFT):
            self.vx -= PLAYER_ACCEL
        if cpygfx.is_key_down(KEY_D) or cpygfx.is_key_down(KEY_RIGHT):
            self.vx += PLAYER_ACCEL

        # 2. 應用摩擦力 (讓速度自然衰減)
        self.vx *= PLAYER_FRICTION
        self.vy *= PLAYER_FRICTION

        # 3. 限制最大速度 (避免飛太快失控)
        # 計算目前速度的大小
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > PLAYER_MAX_SPEED:
            scale = PLAYER_MAX_SPEED / speed
            self.vx *= scale
            self.vy *= scale

        # 4. 更新位置
        self.x += self.vx
        self.y += self.vy

        # 5. 邊界檢查 (不讓玩家跑出視窗外)
        if self.x < 0: 
            self.x = 0
            self.vx = 0 # 撞牆反彈或停下
        elif self.x > SCREEN_WIDTH - self.size:
            self.x = SCREEN_WIDTH - self.size
            self.vx = 0
            
        if self.y < 0:
            self.y = 0
            self.vy = 0
        elif self.y > SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
            self.vy = 0

        # 6. 同步更新 Rect (用於碰撞偵測)
        self.update_rect()

    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        c = COLOR_PLAYER
        cpygfx.draw_rect_filled(self.rect.x, self.rect.y, self.rect.w, self.rect.h, c[0], c[1], c[2])

class Wall:
    def __init__(self, x: int, y: int, width: int, height: int, 
                 move_axis: str = None, move_dist: int = 0, move_speed: float = 0):
        self.rect = Rect(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.move_axis = move_axis
        self.move_dist = move_dist
        self.move_speed = move_speed
        
    def update(self):
        if self.move_axis:
            t = cpygfx.get_ticks() / 1000.0
            offset = math.sin(t * self.move_speed) * self.move_dist
            if self.move_axis == 'x':
                self.rect.x = int(self.start_x + offset)
            elif self.move_axis == 'y':
                self.rect.y = int(self.start_y + offset)

    def draw(self):
        c = COLOR_WALL
        cpygfx.draw_rect_filled(self.rect.x, self.rect.y, self.rect.w, self.rect.h, c[0], c[1], c[2])

class Goal:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = Rect(x, y, width, height)

    def draw(self):
        c = COLOR_GOAL
        cpygfx.draw_rect_filled(self.rect.x, self.rect.y, self.rect.w, self.rect.h, c[0], c[1], c[2])