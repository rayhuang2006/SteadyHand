# 檔案名稱: steadyhand/scene.py
import cpygfx
# [新增] 匯入必要的配置與工具
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_PARTICLE_SPARK
from .utils import ParticleSystem

class Scene:
    def __init__(self, game):
        self.game = game
        # [新增] 每個場景現在都內建一個粒子系統
        self.particles = ParticleSystem()

    def update(self):
        # [新增] 全域點擊偵測
        # 無論在哪個場景，只要點擊滑鼠，就觸發一個小的火花特效
        if cpygfx.get_mouse_clicked():
            mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
            # 發射黃色小火花
            self.particles.emit(mx, my, count=8, color=COLOR_PARTICLE_SPARK, size=4, life=20)
            
        # 更新粒子狀態
        self.particles.update()

    def render(self):
        # [新增] 在所有內容的最上層繪製粒子
        self.particles.draw()