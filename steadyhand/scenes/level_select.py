# 檔案名稱: steadyhand/scenes/level_select.py
from ..scene import Scene
from ..config import *
from ..level_manager import LevelManager
import cpygfx
from cpygfx.keys import KEY_ESCAPE, KEY_W, KEY_S, KEY_UP, KEY_DOWN
from ..i18n import tr, _

class LevelSelectScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.level_manager = LevelManager("levels")
        self.cols = 5
        self.btn_size = 100
        self.btn_gap = 30
        self.start_y = 120 
        self.scroll_y = 0
        self.max_scroll = 0
        self.anim_ticks = 0
        self.buttons = []
        self.back_btn_rect = (20, 20, 100, 40)
        self.init_buttons()

    # ... (init_buttons, update, draw_thumbnail, draw_stars 保持不變) ...
    def init_buttons(self):
        real_levels = self.level_manager.get_level_count()
        total_display = max(20, real_levels) 
        
        grid_width = self.cols * self.btn_size + (self.cols - 1) * self.btn_gap
        start_x = (SCREEN_WIDTH - grid_width) // 2
        
        self.buttons = []
        for i in range(total_display):
            r, c = i // self.cols, i % self.cols
            x = start_x + c * (self.btn_size + self.btn_gap)
            y = self.start_y + r * (self.btn_size + self.btn_gap)
            is_real = (i < real_levels)
            is_locked = not self.level_manager.is_level_unlocked(i) if is_real else True
            record = self.level_manager.get_record(i) if is_real else None
            self.buttons.append({
                "base_rect": (x, y, self.btn_size, self.btn_size),
                "level_idx": i,
                "locked": is_locked,
                "real": is_real,
                "record": record
            })
        total_rows = (total_display + self.cols - 1) // self.cols
        content_height = total_rows * (self.btn_size + self.btn_gap)
        self.max_scroll = max(0, content_height - (SCREEN_HEIGHT - self.start_y - 20))

    def update(self):
        super().update()
        self.anim_ticks += 1
        scroll_speed = 15
        if cpygfx.is_key_down(KEY_W) or cpygfx.is_key_down(KEY_UP): self.scroll_y -= scroll_speed
        if cpygfx.is_key_down(KEY_S) or cpygfx.is_key_down(KEY_DOWN): self.scroll_y += scroll_speed
        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
        
        mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
        clicked = cpygfx.get_mouse_clicked()
        
        bbx, bby, bbw, bbh = self.back_btn_rect
        if clicked and (bbx <= mx <= bbx+bbw and bby <= my <= bby+bbh):
            from .menu import MenuScene
            self.game.switch_scene(MenuScene(self.game))
            return

        if clicked:
            for btn in self.buttons:
                if not btn["real"]: continue
                bx, by, bw, bh = btn["base_rect"]
                screen_y = by - self.scroll_y
                if screen_y < 100 or screen_y > SCREEN_HEIGHT: continue
                if (bx <= mx <= bx+bw and screen_y <= my <= screen_y+bh):
                    if not btn["locked"]:
                        from .gameplay import GameplayScene
                        self.game.switch_scene(GameplayScene(self.game, btn["level_idx"]))
                        return

        if cpygfx.is_key_down(KEY_ESCAPE):
            from .menu import MenuScene
            self.game.switch_scene(MenuScene(self.game))

    def draw_thumbnail(self, level_idx, x, y, size):
        raw_data = self.level_manager.get_level_data_raw(level_idx)
        if not raw_data: return
        padding = 10
        available_size = size - (padding * 2)
        scale = available_size / 800.0
        start_x = x + padding
        start_y = y + padding
        for w in raw_data["walls"]:
            wx, wy = int(w["x"] * scale), int(w["y"] * scale)
            ww, wh = int(w["width"] * scale), int(w["height"] * scale)
            ww = max(1, ww); wh = max(1, wh)
            cpygfx.draw_rect_filled(start_x + wx, start_y + wy, ww, wh, 80, 100, 120)
        g = raw_data["goal"]
        gx, gy = int(g["x"] * scale), int(g["y"] * scale)
        gw, gh = int(g["width"] * scale), int(g["height"] * scale)
        cpygfx.draw_rect_filled(start_x + gx, start_y + gy, max(2, gw), max(2, gh), 50, 200, 50)

    def draw_stars(self, x, y, count):
        for i in range(3):
            c = COLOR_STAR_ON if i < count else COLOR_STAR_OFF
            sx = x + i * 15
            cpygfx.draw_rect_filled(sx, y, 8, 8, c[0], c[1], c[2])

    def draw_leaderboard_panel(self, level_idx, x, y):
        """[修正] 優化版排行榜面板"""
        db_lvl = level_idx + 1
        data = self.game.net.get_cached_leaderboard(db_lvl)
        
        if not data and not self.game.net.is_loading:
            self.game.net.fetch_leaderboard_async(db_lvl)
            
        # [修正 1] 加高面板高度到 180 (原本 160)
        w, h = 280, 180
        if x + w > SCREEN_WIDTH: x -= (w + 120)
            
        cpygfx.draw_rect_filled(x, y, w, h, 20, 25, 30)
        cpygfx.draw_rect(x, y, w, h, 0, 255, 255)

        title_str = _("TOP RECORDS") 
        title = f"{title_str} (L-{db_lvl})"
        tw = cpygfx.get_text_width(title)
        tx = x + (w - tw) // 2
        cpygfx.draw_text(title, tx, y + 10, 255, 255, 255)
        
        if not data:
            load_txt = _("LOADING...")
            lw = cpygfx.get_text_width(load_txt)
            lx = x + (w - lw) // 2
            cpygfx.draw_text(load_txt, lx, y + 70, 150, 150, 150)
        else:
            rank_x = x + 15
            name_x = x + 40
            time_end_x = x + w - 15 
            
            for i, row in enumerate(data[:5]):
                y_pos = y + 45 + i * 22
                name = row['name']
                time_str = f"{row['time']}s"
                
                colors = [(255,215,0), (192,192,192), (205,127,50)]
                c = colors[i] if i < 3 else (150,150,150)
                
                cpygfx.draw_text(f"{i+1}.", rank_x, y_pos, c[0], c[1], c[2])
                
                # [修正 2] 放寬截斷限制到 13 個字元
                # "Player-351e..." -> 13 char
                display_name = name
                if len(name) > 13:
                    display_name = name[:12] + "." 
                
                cpygfx.draw_text(display_name, name_x, y_pos, 255, 255, 255)
                
                tw = cpygfx.get_text_width(time_str)
                tx = time_end_x - tw
                cpygfx.draw_text(time_str, tx, y_pos, 0, 255, 255)

    def render(self):
        c = COLOR_GRID
        for x in range(0, SCREEN_WIDTH, 40): cpygfx.draw_line(x, 0, x, SCREEN_HEIGHT, *c)
        for y in range(0, SCREEN_HEIGHT, 40): cpygfx.draw_line(0, y, SCREEN_WIDTH, y, *c)
        
        cpygfx.draw_rect_filled(0, 0, SCREEN_WIDTH, 100, 10, 12, 20)
        cpygfx.draw_line(0, 100, SCREEN_WIDTH, 100, 50, 60, 80)
        
        title = _("SELECT MODULE")
        tw = cpygfx.get_text_width(title)
        tx = (SCREEN_WIDTH - tw) // 2
        cpygfx.draw_text(title, tx, 40, 255, 255, 255)
        
        mx, my = cpygfx.get_mouse_x(), cpygfx.get_mouse_y()
        bbx, bby, bbw, bbh = self.back_btn_rect
        b_hover = (bbx <= mx <= bbx+bbw and bby <= my <= bby+bbh)
        back_txt = _("< BACK")
        
        bw_txt = cpygfx.get_text_width(back_txt)
        bh_txt = cpygfx.get_text_height(back_txt)
        btx = bbx + (bbw - bw_txt)//2
        bty = bby + (bbh - bh_txt)//2 + 2
        
        if b_hover:
            cpygfx.draw_rect(bbx, bby, bbw, bbh, 0, 255, 255)
            cpygfx.draw_text(back_txt, btx, bty, 0, 255, 255)
        else:
            cpygfx.draw_rect(bbx, bby, bbw, bbh, 100, 100, 100)
            cpygfx.draw_text(back_txt, btx, bty, 150, 150, 150)

        active_tooltip = None 
        
        for btn in self.buttons:
            bx, by, bw, bh = btn["base_rect"]
            screen_y = by - self.scroll_y
            
            if screen_y + bh < 0 or screen_y > SCREEN_HEIGHT: continue
            if screen_y < 100: continue

            if btn["locked"]:
                cpygfx.draw_rect_filled(bx, screen_y, bw, bh, 20, 25, 35)
                cpygfx.draw_rect(bx, screen_y, bw, bh, 60, 70, 90)
                cpygfx.draw_line(bx+20, screen_y+20, bx+bw-20, screen_y+bh-20, 60, 70, 90)
                cpygfx.draw_line(bx+bw-20, screen_y+20, bx+20, screen_y+bh-20, 60, 70, 90)
            else:
                hover = (bx <= mx <= bx+bw and screen_y <= my <= screen_y+bh)
                border_c = COLOR_UI_BORDER_HOVER if hover else COLOR_UI_NORMAL
                
                cpygfx.draw_rect_filled(bx, screen_y, bw, bh, 30, 35, 50)
                cpygfx.draw_rect(bx, screen_y, bw, bh, border_c[0], border_c[1], border_c[2])
                
                if btn["real"]:
                    self.draw_thumbnail(btn["level_idx"], bx, screen_y, bw)
                    if btn["record"]:
                        self.draw_stars(bx + 10, screen_y + bh - 20, btn["record"]["stars"])
                    else:
                        cpygfx.draw_text(_("NEW"), bx + 10, screen_y + bh - 30, 0, 255, 255)
                    
                    if hover:
                        active_tooltip = (btn["level_idx"], bx + 110, screen_y)
                        
                num_str = str(btn["level_idx"]+1)
                num_w = cpygfx.get_text_width(num_str)
                cpygfx.draw_text(num_str, bx + bw - num_w - 5, screen_y + 5, 200, 200, 200)

        if active_tooltip:
            self.draw_leaderboard_panel(*active_tooltip)
