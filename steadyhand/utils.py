# 檔案名稱: steadyhand/utils.py
import cpygfx
import random
import math

class Rect:
    def __init__(self, x, y, w, h):
        self.x = int(x); self.y = int(y); self.w = int(w); self.h = int(h)

def check_collision(rect1: Rect, rect2: Rect) -> bool:
    return cpygfx.check_collision(rect1.x, rect1.y, rect1.w, rect1.h, rect2.x, rect2.y, rect2.w, rect2.h)

# --- [新增] 螢幕震動管理器 ---
class ScreenShaker:
    def __init__(self):
        self.shake_strength = 0
        self.shake_decay = 0.9 # 衰減速度
        self.offset_x = 0
        self.offset_y = 0

    def trigger(self, strength):
        self.shake_strength = strength

    def update(self):
        if self.shake_strength > 0.5:
            # 隨機產生偏移
            self.offset_x = int((random.random() * 2 - 1) * self.shake_strength)
            self.offset_y = int((random.random() * 2 - 1) * self.shake_strength)
            self.shake_strength *= self.shake_decay
        else:
            self.shake_strength = 0
            self.offset_x = 0
            self.offset_y = 0

# --- [新增] 粒子系統 ---
class Particle:
    def __init__(self, x, y, color, size, life):
        self.x = x
        self.y = y
        self.vx = (random.random() * 2 - 1) * 3 # 隨機速度 X
        self.vy = (random.random() * 2 - 1) * 3 # 隨機速度 Y
        self.color = color
        self.size = size
        self.life = life # 生命週期 (Frames)
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(0, self.size - 0.1) # 慢慢變小

    def draw(self):
        if self.life > 0 and self.size > 0:
            # 根據壽命模擬亮度/透明度
            fade = self.life / self.max_life
            r = int(self.color[0] * fade)
            g = int(self.color[1] * fade)
            b = int(self.color[2] * fade)
            cpygfx.draw_rect_filled(int(self.x), int(self.y), int(self.size), int(self.size), r, g, b)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count, color, size=4, life=30):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, size, life))

    def update(self):
        # 更新並移除死掉的粒子
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def draw(self):
        for p in self.particles:
            p.draw()