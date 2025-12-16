# 檔案名稱: steadyhand/game.py
import cpygfx
# [修正] 匯入 SERVER_HOST, SERVER_PORT
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, COLOR_BG, COLOR_TRANSITION, COLOR_GRID, SERVER_HOST, SERVER_PORT, DEFAULT_LANG
from .scenes.menu import MenuScene
from .network_client import NetworkClient
from . import i18n

class Game:
    def __init__(self):
        if not cpygfx.load_font(FONT_PATH, 24):
            print("Warning: Font loading failed.")
            
        self.running = True
        
        # [修正] 使用 Config 裡的設定，不再寫死 IP
        print(f"[Game] Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")
        self.net = NetworkClient(host=SERVER_HOST, port=SERVER_PORT)
        
        self.current_scene = MenuScene(self)
        self.next_scene_buffer = None 
        
        self.transition_state = 'NONE'
        self.transition_width = 0 
        self.max_trans_width = (SCREEN_WIDTH // 2) + 10
        self.trans_speed = 12 
        self.hold_ticks = 0
        self.hold_duration = 30 

        # 設置語言
        i18n.set_language(DEFAULT_LANG)
        
        print("Engine initialized: Geometry Mode + Network.")

    def switch_scene(self, new_scene):
        if self.transition_state == 'NONE':
            self.next_scene_buffer = new_scene
            self.transition_state = 'CLOSING'

    def update_transition(self):
        if self.transition_state == 'CLOSING':
            self.transition_width += self.trans_speed
            if self.transition_width >= self.max_trans_width:
                self.transition_width = self.max_trans_width
                if self.next_scene_buffer:
                    self.current_scene = self.next_scene_buffer
                    self.next_scene_buffer = None
                self.transition_state = 'HOLD'
                self.hold_ticks = self.hold_duration
                
        elif self.transition_state == 'HOLD':
            self.hold_ticks -= 1
            if self.hold_ticks <= 0:
                self.transition_state = 'OPENING'
                
        elif self.transition_state == 'OPENING':
            self.transition_width -= self.trans_speed
            if self.transition_width <= 0:
                self.transition_width = 0
                self.transition_state = 'NONE'

    def render_transition(self):
        if self.transition_state != 'NONE':
            w = int(self.transition_width)
            h = SCREEN_HEIGHT
            c = COLOR_TRANSITION
            cpygfx.draw_rect_filled(0, 0, w, h, c[0], c[1], c[2])
            cpygfx.draw_rect_filled(SCREEN_WIDTH - w, 0, w, h, c[0], c[1], c[2])
            line_c = (100, 100, 120)
            cpygfx.draw_rect(w-2, 0, 2, h, line_c[0], line_c[1], line_c[2])
            cpygfx.draw_rect(SCREEN_WIDTH - w, 0, 2, h, line_c[0], line_c[1], line_c[2])

    def render_global_background(self):
        c = COLOR_BG
        cpygfx.clear(c[0], c[1], c[2])
        gc = COLOR_GRID
        for x in range(0, SCREEN_WIDTH, 40):
            cpygfx.draw_line(x, 0, x, SCREEN_HEIGHT, gc[0], gc[1], gc[2])
        for y in range(0, SCREEN_HEIGHT, 40):
            cpygfx.draw_line(0, y, SCREEN_WIDTH, y, gc[0], gc[1], gc[2])

    def run(self):
        while self.running:
            cpygfx.delay(16)
            if cpygfx.poll_event():
                self.running = False
            self.current_scene.update()
            self.update_transition()
            self.render_global_background()
            self.current_scene.render()
            self.render_transition()
            cpygfx.update()
