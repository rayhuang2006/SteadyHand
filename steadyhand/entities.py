import cpygfx
from .config import COLOR_PLAYER, COLOR_WALL, COLOR_GOAL
from .utils import Rect

class Player:
    """ (Player 類別沒有變動) """
    def __init__(self, x: int, y: int, size: int):
        self.size = size
        self.radius = size // 2
        # 我們將使用 Rect 來儲存位置和大小
        self.rect = Rect(x - self.radius, y - self.radius, size, size)

    def set_pos(self, x: int, y: int):
        self.rect.x = x - self.radius
        self.rect.y = y - self.radius

    def draw(self):
        c = COLOR_PLAYER
        # 呼叫 CPyGfx V2 的函式
        cpygfx.draw_rect_filled(self.rect.x, self.rect.y, self.rect.w, self.rect.h, c[0], c[1], c[2])

class Wall:
    def __init__(self, x: int, y: int, width: int, height: int): # <-- (修正點 1)
        self.rect = Rect(x, y, width, height)                    # <-- (修正點 2)

    def draw(self):
        c = COLOR_WALL
        cpygfx.draw_rect_filled(self.rect.x, self.rect.y, self.rect.w, self.rect.h, c[0], c[1], c[2])

class Goal:
    def __init__(self, x: int, y: int, width: int, height: int): # <-- (修正點 3)
        self.rect = Rect(x, y, width, height)                    # <-- (修正點 4)

    def draw(self):
        c = COLOR_GOAL
        cpygfx.draw_rect_filled(self.rect.x, self.rect.y, self.rect.w, self.rect.h, c[0], c[1], c[2])