class Rect:
    """ 一個簡單的矩形類別，用於碰撞偵測 """
    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)

def check_collision(rect1: Rect, rect2: Rect) -> bool:
    """
    AABB 碰撞偵測 (Axis-Aligned Bounding Box)
    (因為你的 V2 函式庫沒有提供碰撞偵測，我們在 Python 中實作)
    """
    # 檢查 rect1 是否在 rect2 的左側
    if rect1.x + rect1.w <= rect2.x:
        return False
    # 檢查 rect1 是否在 rect2 的右側
    if rect1.x >= rect2.x + rect2.w:
        return False
    # 檢查 rect1 是否在 rect2 的上方
    if rect1.y + rect1.h <= rect2.y:
        return False
    # 檢查 rect1 是否在 rect2 的下方
    if rect1.y >= rect2.y + rect2.h:
        return False
    
    # 如果以上都不是，則必定發生碰撞
    return True