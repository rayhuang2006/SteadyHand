# 檔案名稱: steadyhand/level_manager.py
import os
import json
from .entities import Wall, Goal

class LevelManager:
    # 建立一個單例模式或靜態儲存，確保成績在場景切換間保留
    _save_data = {} # 格式: { level_index: {"stars": int, "time": float} }

    def __init__(self, level_dir: str):
        self.level_dir = level_dir
        self.levels = [] # 緩存所有關卡資料 (為了縮圖)
        self.load_all_levels()

    def load_all_levels(self):
        """預先讀取所有關卡 JSON，方便選單畫縮圖"""
        try:
            files = [f for f in os.listdir(self.level_dir) if f.endswith('.json')]
            files.sort()
            
            for f in files:
                filepath = os.path.join(self.level_dir, f)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    self.levels.append(data)
                    
            print(f"LevelManager cached {len(self.levels)} levels.")
        except FileNotFoundError:
            print(f"錯誤：找不到關卡目錄 '{self.level_dir}'")

    def get_level_count(self) -> int:
        return len(self.levels)

    def get_level_data_raw(self, index):
        """取得原始字典資料 (給縮圖用)"""
        if 0 <= index < len(self.levels):
            return self.levels[index]
        return None

    def load_level_entities(self, index):
        """將原始資料轉換為實體物件 (給遊戲用)"""
        raw = self.get_level_data_raw(index)
        if not raw: return None
        
        return {
            "walls": [Wall(**w) for w in raw["walls"]],
            "goal": Goal(**raw["goal"]),
            "start_pos": tuple(raw["start_pos"])
        }

    # --- 成績存取系統 ---
    def save_record(self, level_idx, time_spent, stars):
        # 如果已經有紀錄，只保留較好的 (時間更短或星星更多)
        if level_idx in self._save_data:
            old_record = self._save_data[level_idx]
            if stars > old_record["stars"] or (stars == old_record["stars"] and time_spent < old_record["time"]):
                self._save_data[level_idx] = {"stars": stars, "time": time_spent}
        else:
            self._save_data[level_idx] = {"stars": stars, "time": time_spent}
            
        # (未來可以在這裡寫入 save.json 檔案)

    def get_record(self, level_idx):
        return self._save_data.get(level_idx, None)

    def is_level_unlocked(self, level_idx):
        # 第 1 關永遠解鎖
        if level_idx == 0: return True
        # 如果上一關有紀錄，則此關解鎖
        return (level_idx - 1) in self._save_data