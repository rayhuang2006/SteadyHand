# 檔案名稱: steadyhand/scenes/gameplay.py
from ..scene import Scene
from ..config import *
from ..entities import Player, Wall, Goal
from ..level_manager import LevelManager
# [修正] 移除 ParticleSystem 的匯入，因為 base scene 已經處理了
from ..utils import check_collision, ScreenShaker 
import cpygfx
from cpygfx.keys import KEY_ESCAPE, KEY_ENTER, KEY_R

class GameplayScene(Scene):
    def __init__(self, game, level_index):
        super().__init__(game)
        self.level_index = level_index
        self.level_manager = LevelManager("levels")
        self.player = None; self.walls = []; self.goal = None
        self.state = "PLAYING" 
        self.start_ticks = cpygfx.get_ticks()
        self.pause_start_tick = 0 
        self.final_time = 0.0
        self.earned_stars = 0
        self.delay_timer = 0
        # [修正] 移除 self.particles = ParticleSystem() (父類別已建立)
        self.shaker = ScreenShaker()
        
        # [關鍵修正] 將暫停按鈕移到左上角
        # 原本: (SCREEN_WIDTH - 60, 40, 40, 40)
        # 改為: (左邊距 20, 頂邊距 40, 寬 40, 高 40)
        self.pause_btn_rect = (20, 40, 40, 40)
        
        # 按鈕位置 (保持不變，Y=200)
        self.overlay_btn_retry = (40, 200, 200, 50)
        self.overlay_btn_menu = (260, 200, 200, 50)
        self.overlay_btn_resume = (150, 200, 200, 50)

        self.load_level()

    # ... (load_level, get_current_time, calculate_stars, trigger_pause, trigger_resume 保持不變) ...
    def load_level(self):
        data = self.level_manager.load_level_entities(self.level_index)
        if not data: return
        self.player = Player(data["start_pos"][0], data["start_pos"][1])
        self.walls = data["walls"]
        self.goal = data["goal"]

    def get_current_time(self):
        if self.state == "WIN" or self.state == "WINNING": return self.final_time
        return (cpygfx.get_ticks() - self.start_ticks) / 1000.0

    def calculate_stars(self, time):
        if time <= STAR_3_TIME: return 3
        if time <= STAR_2_TIME: return 2
        return 1

    def trigger_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
            self.pause_start_tick = cpygfx.get_ticks()

    def trigger_resume(self):
        if self.state == "PAUSED":
            self.state = "PLAYING"
            paused_duration = cpygfx.get_ticks() - self.pause_start_tick
            self.start_ticks += paused_duration

    def update(self):
        # [新增] 呼叫父類別的 update 以處理全域點擊特效
        super().update()
        
        if cpygfx.is_key_down(KEY_ESCAPE):
            if self.state == "PLAYING": self.trigger_pause()
            elif self.state == "PAUSED": self.trigger_resume()
            cpygfx.delay(200) 

        self.shaker.update()
        # [修正] 移除 self.particles.update() (父類別已處理)
        
        mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
        clicked = cpygfx.get_mouse_clicked()

        if self.state == "PLAYING":
            pbx, pby, pbw, pbh = self.pause_btn_rect
            if clicked and (pbx <= mx <= pbx+pbw and pby <= my <= pby+pbh):
                self.trigger_pause()
                return

            self.player.update()
            if cpygfx.get_ticks() % 5 == 0: 
                self.particles.emit(self.player.x + 8, self.player.y + 8, 1, COLOR_PLAYER_TRAIL, size=3, life=15)

            for wall in self.walls: wall.update()
            
            p_rect = self.player.rect
            for wall in self.walls:
                if check_collision(p_rect, wall.rect):
                    self.state = "DYING"
                    self.delay_timer = 60 
                    self.shaker.trigger(15)
                    self.particles.emit(self.player.x, self.player.y, 30, COLOR_PARTICLE_SPARK, size=6, life=50)
                    return
            
            if self.goal and check_collision(p_rect, self.goal.rect):
                self.state = "WINNING"
                self.delay_timer = 60
                self.final_time = (cpygfx.get_ticks() - self.start_ticks) / 1000.0
                self.earned_stars = self.calculate_stars(self.final_time)
                self.level_manager.save_record(self.level_index, self.final_time, self.earned_stars)
                self.particles.emit(self.player.x, self.player.y, 30, (100, 255, 100), size=5, life=60)
                return

        elif self.state == "DYING":
            self.delay_timer -= 1
            if self.delay_timer <= 0: self.state = "DEAD"

        elif self.state == "WINNING":
            self.delay_timer -= 1
            if self.delay_timer <= 0: self.state = "WIN"

        elif self.state in ["PAUSED", "DEAD", "WIN"]:
            ow, oh = 500, 300
            ox = (SCREEN_WIDTH - ow) // 2
            oy = (SCREEN_HEIGHT - oh) // 2
            
            if self.state == "PAUSED":
                rbx, rby, rbw, rbh = self.overlay_btn_resume
                if clicked and (ox+rbx <= mx <= ox+rbx+rbw and oy+rby <= my <= oy+rby+rbh):
                    self.trigger_resume()
                    return
            else:
                rbx, rby, rbw, rbh = self.overlay_btn_retry
                if clicked and (ox+rbx <= mx <= ox+rbx+rbw and oy+rby <= my <= oy+rby+rbh):
                    self.load_level()
                    self.state = "PLAYING"
                    self.start_ticks = cpygfx.get_ticks()
                    return
                mbx, mby, mbw, mbh = self.overlay_btn_menu
                if clicked and (ox+mbx <= mx <= ox+mbx+mbw and oy+mby <= my <= oy+mby+mbh):
                    from .level_select import LevelSelectScene
                    self.game.switch_scene(LevelSelectScene(self.game))
                    return
            
            if cpygfx.is_key_down(KEY_R) and self.state != "WIN":
                 self.load_level(); self.state = "PLAYING"; self.start_ticks = cpygfx.get_ticks()

    # ... (draw_button, draw_interactive_overlay 保持不變，已完美置中) ...
    def draw_button(self, x, y, w, h, text, hover=False, highlight_color=COLOR_UI_HOVER):
        c = highlight_color if hover else COLOR_UI_NORMAL
        cpygfx.draw_rect_filled(x, y, w, h, 30, 35, 50)
        cpygfx.draw_rect(x, y, w, h, c[0], c[1], c[2])
        tw = cpygfx.get_text_width(text)
        th = cpygfx.get_text_height(text)
        tx = x + (w - tw) // 2
        ty = y + (h - th) // 2
        cpygfx.draw_text(text, tx, ty, c[0], c[1], c[2])

    def render(self):
        sx, sy = self.shaker.offset_x, self.shaker.offset_y
        for x in range(0, SCREEN_WIDTH, 40): cpygfx.draw_line(x+sx, 0+sy, x+sx, SCREEN_HEIGHT+sy, *COLOR_GRID)
        for y in range(0, SCREEN_HEIGHT, 40): cpygfx.draw_line(0+sx, y+sy, SCREEN_WIDTH+sx, y+sy, *COLOR_GRID)

        for wall in self.walls: wall.draw()
        if self.goal: self.goal.draw()
        if self.state not in ["DYING", "DEAD", "WINNING", "WIN"]: self.player.draw()
        
        # [修正] 移除 self.particles.draw() (父類別會統一在最後繪製)
        
        if self.state == "PLAYING":
            time_display = self.get_current_time()
            t_str = f"TIME: {time_display:.2f}"
            tw = cpygfx.get_text_width(t_str)
            # 時間顯示在右側
            cpygfx.draw_text(t_str, SCREEN_WIDTH - tw - 20, 45, 255, 255, 255)
            
            mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
            pbx, pby, pbw, pbh = self.pause_btn_rect
            phover = (pbx <= mx <= pbx+pbw and pby <= my <= pby+pbh)
            c = COLOR_UI_HOVER if phover else COLOR_UI_NORMAL
            # 繪製左上角的暫停按鈕
            cpygfx.draw_rect(pbx, pby, pbw, pbh, c[0], c[1], c[2])
            cpygfx.draw_rect_filled(pbx+12, pby+10, 6, 20, c[0], c[1], c[2])
            cpygfx.draw_rect_filled(pbx+22, pby+10, 6, 20, c[0], c[1], c[2])
        
        if self.state == "DEAD":
            self.draw_interactive_overlay("CRITICAL FAILURE", (255, 50, 50))
        elif self.state == "WIN":
            self.draw_interactive_overlay("SEQUENCE COMPLETE", (50, 255, 50), show_stars=True)
        elif self.state == "PAUSED":
            cpygfx.draw_rect_filled(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            self.draw_interactive_overlay("SYSTEM PAUSED", (255, 255, 0), is_pause_menu=True)
        
        # [新增] 呼叫父類別 render 以繪製全域粒子
        super().render()

    def draw_interactive_overlay(self, title, color, show_stars=False, is_pause_menu=False):
        w, h = 500, 300 
        x = (SCREEN_WIDTH - w) // 2
        y = (SCREEN_HEIGHT - h) // 2
        
        mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
        
        cpygfx.draw_rect_filled(x, y, w, h, 20, 20, 30)
        cpygfx.draw_rect(x, y, w, h, color[0], color[1], color[2])
        
        tw = cpygfx.get_text_width(title)
        text_x = x + (w - tw) // 2
        cpygfx.draw_text(title, text_x, y + 40, color[0], color[1], color[2])
        
        content_y = y + 90
        if show_stars:
            gap = 60
            start_star_x = x + (w - (3*20 + 2*gap)) // 2 + 10
            for i in range(3):
                sx = start_star_x + i * gap
                c_star = COLOR_STAR_ON if i < self.earned_stars else COLOR_STAR_OFF
                cpygfx.draw_rect_filled(sx, content_y, 20, 20, c_star[0], c_star[1], c_star[2])
                cpygfx.draw_rect(sx, content_y, 20, 20, 255, 255, 255)
            
            time_str = f"FINAL TIME: {self.final_time:.2f}s"
            ttw = cpygfx.get_text_width(time_str)
            tx = x + (w - ttw)//2
            cpygfx.draw_text(time_str, tx, content_y + 50, 200, 200, 200)
            
        if is_pause_menu:
            rbx, rby, rbw, rbh = self.overlay_btn_resume
            rhover = (x+rbx <= mx <= x+rbx+rbw and y+rby <= my <= y+rby+rbh)
            self.draw_button(x+rbx, y+rby, rbw, rbh, "RESUME GAME", rhover)
        else:
            rbx, rby, rbw, rbh = self.overlay_btn_retry
            rhover = (x+rbx <= mx <= x+rbx+rbw and y+rby <= my <= y+rby+rbh)
            self.draw_button(x+rbx, y+rby, rbw, rbh, "RETRY", rhover)
            
            mbx, mby, mbw, mbh = self.overlay_btn_menu
            mhover = (x+mbx <= mx <= x+mbx+mbw and y+mby <= my <= y+mby+mbh)
            self.draw_button(x+mbx, y+mby, mbw, mbh, "MAIN MENU", mhover)