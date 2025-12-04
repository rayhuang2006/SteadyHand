# 檔案名稱: steadyhand/utils.py
import cpygfx
import random
import math
import os

# [新增] 手刻 .env 解析器
def load_env_file(filepath=".env"):
    """
    讀取 .env 檔案並回傳字典。
    支援格式: KEY=VALUE
    忽視以 # 開頭的註解。
    """
    config = {}
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                # 忽略空行和註解
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    return config

class Rect:
    def __init__(self, x, y, w, h):
        self.x = int(x); self.y = int(y); self.w = int(w); self.h = int(h)

def check_collision(rect1: Rect, rect2: Rect) -> bool:
    return cpygfx.check_collision(rect1.x, rect1.y, rect1.w, rect1.h, rect2.x, rect2.y, rect2.w, rect2.h)

class ScreenShaker:
    def __init__(self):
        self.shake_strength = 0
        self.shake_decay = 0.9
        self.offset_x = 0
        self.offset_y = 0

    def trigger(self, strength):
        self.shake_strength = strength

    def update(self):
        if self.shake_strength > 0.5:
            self.offset_x = int((random.random() * 2 - 1) * self.shake_strength)
            self.offset_y = int((random.random() * 2 - 1) * self.shake_strength)
            self.shake_strength *= self.shake_decay
        else:
            self.shake_strength = 0
            self.offset_x = 0
            self.offset_y = 0

class Particle:
    def __init__(self, x, y, color, size, life):
        self.x = x; self.y = y
        self.vx = (random.random() * 2 - 1) * 3
        self.vy = (random.random() * 2 - 1) * 3
        self.color = color; self.size = size
        self.life = life; self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self):
        if self.life > 0 and self.size > 0:
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
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles: p.update()

    def draw(self):
        for p in self.particles: p.draw()