import os
import json
from .entities import Wall, Goal

class LevelManager:
    def __init__(self, level_dir: str):
        self.level_dir = level_dir
        self.level_files = []
        try:
            # 載入所有 .json 檔案並排序
            files = [f for f in os.listdir(level_dir) if f.endswith('.json')]
            files.sort()
            self.level_files = [os.path.join(level_dir, f) for f in files]
        except FileNotFoundError:
            print(f"錯誤：找不到關卡目錄 '{level_dir}'")
            
        print(f"找到了 {len(self.level_files)} 個關卡。")

    def get_level_count(self) -> int:
        return len(self.level_files)

    def load_level_data(self, level_index: int):
        """
        載入關卡並回傳遊戲物件
        """
        if level_index < 0 or level_index >= len(self.level_files):
            print(f"錯誤：關卡索引 {level_index} 無效。")
            return None

        filepath = self.level_files[level_index]
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # 將 JSON 資料轉換為我們的遊戲物件
            walls = [Wall(**w) for w in data["walls"]]
            goal = Goal(**data["goal"])
            start_pos = tuple(data["start_pos"])
            
            print(f"成功載入關卡: {filepath}")
            return {
                "walls": walls,
                "goal": goal,
                "start_pos": start_pos
            }
            
        except Exception as e:
            print(f"載入關卡 {filepath} 失敗: {e}")
            return None