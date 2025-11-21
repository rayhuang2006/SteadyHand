import cpygfx

class Rect:
    """ 一個簡單的矩形類別 """
    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)

def check_collision(rect1: Rect, rect2: Rect) -> bool:
    """
    使用 CPyGfx 的 C 核心進行碰撞偵測
    """
    return cpygfx.check_collision(
        rect1.x, rect1.y, rect1.w, rect1.h,
        rect2.x, rect2.y, rect2.w, rect2.h
    )