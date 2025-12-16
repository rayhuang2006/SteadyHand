# 檔案名稱: steadyhand/scenes/menu.py
from ..scene import Scene
from ..config import *
# [修正] 移除 ParticleSystem 匯入
import cpygfx
from cpygfx.keys import KEY_ENTER
from ..i18n import tr, _

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.start_button_rect = (200, 380, 400, 60)
        self.anim_ticks = 0
        # [修正] 移除 self.particles = ParticleSystem() (父類別已建立)
        self.last_mx = 0
        self.last_my = 0

    def update(self):
        # [新增] 呼叫父類別 update 以處理全域點擊特效
        super().update()
        
        self.anim_ticks += 1
        mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
        clicked = cpygfx.get_mouse_clicked()
        enter_pressed = cpygfx.is_key_down(KEY_ENTER)
        
        # 選單專屬的滑鼠拖尾特效 (仍然保留)
        if abs(mx - self.last_mx) > 2 or abs(my - self.last_my) > 2:
            self.particles.emit(mx, my, 1, COLOR_PARTICLE_TRAIL, size=3, life=20)
        self.last_mx, self.last_my = mx, my
        
        # [修正] 移除 self.particles.update() (父類別已處理)
        
        bx, by, bw, bh = self.start_button_rect
        hover = (bx <= mx <= bx+bw and by <= my <= by+bh)
        
        if (hover and clicked) or enter_pressed:
            # 按鈕點擊的大爆炸特效 (仍然保留，會與全域點擊疊加)
            self.particles.emit(mx, my, 10, COLOR_PARTICLE_SPARK, size=5, life=30)
            from .level_select import LevelSelectScene
            self.game.switch_scene(LevelSelectScene(self.game))
            cpygfx.delay(200)

    def draw_dynamic_background(self):
        # ... (保持不變) ...
        grid_size = 40
        scroll_x = int(self.anim_ticks * 0.5) % grid_size
        scroll_y = int(self.anim_ticks * 0.5) % grid_size
        c = COLOR_GRID
        for x in range(-grid_size, SCREEN_WIDTH, grid_size):
            draw_x = x + scroll_x
            cpygfx.draw_line(draw_x, 0, draw_x, SCREEN_HEIGHT, c[0], c[1], c[2])
        for y in range(-grid_size, SCREEN_HEIGHT, grid_size):
            draw_y = y + scroll_y
            cpygfx.draw_line(0, draw_y, SCREEN_WIDTH, draw_y, c[0], c[1], c[2])

    def render(self):
        self.draw_dynamic_background()
        
        # 標題
        t1 = tr("STEADY HAND")
        tw1 = cpygfx.get_text_width(t1)
        cpygfx.draw_text(t1, (SCREEN_WIDTH - tw1)//2, 150, 255, 255, 255)
        
        t2 = tr("SYSTEM READY // AWAITING INPUT")
        tw2 = cpygfx.get_text_width(t2)
        sub = COLOR_UI_NORMAL
        cpygfx.draw_text(t2, (SCREEN_WIDTH - tw2)//2, 220, sub[0], sub[1], sub[2])
        
        # 按鈕
        mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
        bx, by, bw, bh = self.start_button_rect
        hover = (bx <= mx <= bx+bw and by <= my <= by+bh)
        
        if hover:
            c = COLOR_UI_HOVER
            text = tr("> INITIALIZE PROTOCOL <")
            cpygfx.draw_rect_filled(bx, by, bw, bh, 20, 40, 50) 
            cpygfx.draw_rect(bx, by, bw, bh, c[0], c[1], c[2])
        else:
            c = COLOR_UI_NORMAL
            text = tr("INITIALIZE PROTOCOL")

        tw = cpygfx.get_text_width(text)
        th = cpygfx.get_text_height(text)
        
        tx = bx + (bw - tw) // 2
        ty = by + (bh - th) // 2
        
        cpygfx.draw_text(text, tx, ty, c[0], c[1], c[2])
        
        # [新增] 呼叫父類別 render 以繪製全域粒子
        super().render()
