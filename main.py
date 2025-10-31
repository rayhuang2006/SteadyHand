import sys
import cpygfx
from steadyhand.game import Game
from steadyhand.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    """
    主函式：
    1. 初始化 CPyGfx 函式庫
    2. 建立並執行遊戲
    3. 清理 CPyGfx 資源
    """
    
    # 1. 初始化 CPyGfx
    # ---------------------------------------------
    if not cpygfx.init_window(SCREEN_WIDTH, SCREEN_HEIGHT):
        print("錯誤：無法初始化 CPyGfx 視窗", file=sys.stderr)
        return 1
        
    if not cpygfx.text_init():
        print("錯誤：無法初始化 CPyGfx 文字 (TTF) 模組", file=sys.stderr)
        cpygfx.close_window()
        return 1
        
    # (可選) 初始化圖片模組，即使我們還沒用
    if not cpygfx.image_init():
        print("警告：無法初始化 CPyGfx 圖片 (Image) 模組", file=sys.stderr)
    
    print("CPyGfx 函式庫初始化成功。")
    
    # 2. 建立並執行遊戲
    # ---------------------------------------------
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"遊戲執行時發生未預期錯誤: {e}", file=sys.stderr)
        # 顯示 traceback 資訊
        import traceback
        traceback.print_exc()
    finally:
        # 3. 清理 CPyGfx 資源
        # ---------------------------------------------
        print("正在關閉 CPyGfx...")
        cpygfx.image_quit()
        cpygfx.text_quit()
        cpygfx.close_window()
        
    return 0

if __name__ == "__main__":
    sys.exit(main())