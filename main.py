# 檔案名稱: main.py
import sys
import cpygfx
from steadyhand.game import Game
from steadyhand.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    # 1. 初始化視窗 (最優先)
    if not cpygfx.init_window(SCREEN_WIDTH, SCREEN_HEIGHT):
        return 1
    
    # 2. 初始化文字引擎
    if not cpygfx.text_init():
        return 1
    
    # 3. [修正] 初始化圖片引擎 (之前漏了這行，導致無法載入背景圖)
    if not cpygfx.image_init():
        print("警告：圖片引擎初始化失敗")
        # 這裡不 return，因為就算沒圖片，我們也有 fallback 顏色
    
    # 4. 啟動遊戲
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Game Crashed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 5. 清理資源
        cpygfx.image_quit()
        cpygfx.text_quit()
        cpygfx.close_window()
        
    return 0

if __name__ == "__main__":
    sys.exit(main())