# 檔案名稱: server/db_engine.py
import struct
import os
import threading
import time

class SteadyHandDB:
    """
    全自研二進位資料庫引擎 (Binary Database Engine)
    專門用於儲存 SteadyHand 的玩家成績。
    不依賴 SQL，直接操作 Bytes。
    """
    
    def __init__(self, db_file="steadyhand.db"):
        self.db_file = db_file
        self.lock = threading.Lock() # 線程鎖，防止多人同時寫入時檔案壞掉
        
        # --- [核心] 資料結構定義 (Schema) ---
        # 我們使用 struct 模組的格式字串來定義每一筆紀錄的樣子
        # 格式: "16s I f I d"
        # 16s: user_name (16 bytes 字串，固定長度)
        # I:   level_id (4 bytes unsigned int)
        # f:   time_spent (4 bytes float)
        # I:   stars (4 bytes unsigned int)
        # d:   timestamp (8 bytes double)
        # -----------------------------------
        # 總長度 = 16 + 4 + 4 + 4 + 8 = 36 bytes / record
        self.format = "16sIfId" 
        self.record_size = struct.calcsize(self.format)
        
        # 初始化：確保檔案存在
        if not os.path.exists(self.db_file):
            with open(self.db_file, "wb") as f:
                pass # 建立空檔案
        
        print(f"[DB] Engine initialized. Record size: {self.record_size} bytes")

    def add_score(self, username: str, level_id: int, time_spent: float, stars: int):
        """
        寫入一筆新成績 (Append Only)
        """
        # 1. 資料處理
        # 確保 username 是 bytes，且長度剛好 16 (不足補 \x00，太長切掉)
        name_bytes = username.encode('utf-8')[:16].ljust(16, b'\x00')
        timestamp = time.time()
        
        # 2. 打包成二進位 (Pack)
        # 這裡會把所有資料變成一串看不懂的 bytes，例如 b'Ray\x00...\x00\x01\x00...'
        data = struct.pack(self.format, name_bytes, level_id, time_spent, stars, timestamp)
        
        # 3. 寫入檔案 (Thread-Safe)
        with self.lock:
            with open(self.db_file, "ab") as f: # 'ab' = Append Binary
                f.write(data)
                
        print(f"[DB] Inserted score: {username} - Lv.{level_id} - {time_spent:.2f}s")

    def get_leaderboard(self, level_id: int, limit=5):
        """
        讀取排行榜 (全表掃描並排序)
        """
        records = []
        
        with self.lock:
            with open(self.db_file, "rb") as f:
                while True:
                    # 1. 每次讀取固定長度 (36 bytes)
                    chunk = f.read(self.record_size)
                    if not chunk: 
                        break # 讀到檔尾停止
                    
                    # 2. 解包 (Unpack)
                    try:
                        name_b, lvl, t, star, ts = struct.unpack(self.format, chunk)
                    except struct.error:
                        print("[DB] Warning: Corrupted record found, skipping.")
                        continue
                    
                    # 3. 篩選：只取目前關卡的資料
                    if lvl == level_id:
                        # 清理名字 (把後面的 \x00 拿掉)
                        clean_name = name_b.decode('utf-8').rstrip('\x00')
                        records.append({
                            "name": clean_name,
                            "time": round(t, 2),
                            "stars": star,
                            "date": time.ctime(ts) # 轉成可讀時間
                        })
        
        # 4. 排序與取前幾名
        # 規則：時間越短越好 (Ascending)
        records.sort(key=lambda x: x["time"])
        
        # 5. 去重 (選用)：如果同一個人有多筆成績，只留最好的
        # 這裡簡單實作：用 dict 過濾
        best_scores = {}
        for r in records:
            name = r["name"]
            if name not in best_scores:
                best_scores[name] = r
            # 因為已經排過序了，先出現的一定是比較好的，所以不用做比較
            
        final_list = list(best_scores.values())
        return final_list[:limit]

# --- 測試區 (當直接執行此檔案時運作) ---
if __name__ == "__main__":
    # [修正 1] 使用正式檔名，方便 db_viewer 讀取
    db_filename = "steadyhand.db"
    
    # 如果想從乾淨的狀態開始，先刪除舊的
    if os.path.exists(db_filename):
        os.remove(db_filename)
        
    db = SteadyHandDB(db_filename)
    
    print("--- 寫入測試數據 ---")
    db.add_score("Ray", 1, 12.5, 3)
    db.add_score("Alice", 1, 9.8, 3)
    db.add_score("Bob", 1, 15.2, 2)
    db.add_score("Ray", 1, 8.5, 3) 
    db.add_score("Hacker", 2, 0.1, 3) 
    
    print("\n--- 讀取 Level 1 排行榜 ---")
    top5 = db.get_leaderboard(1)
    for i, r in enumerate(top5):
        print(f"Rank {i+1}: {r['name']} - {r['time']}s ({r['stars']} stars)")
        
    print("\n--- 讀取 Level 2 排行榜 ---")
    top5_lv2 = db.get_leaderboard(2)
    for i, r in enumerate(top5_lv2):
        print(f"Rank {i+1}: {r['name']} - {r['time']}s")
    
    # [修正 2] 註解掉刪除指令，讓檔案保留下來
    # os.remove(db_filename) 
    print(f"\n[DB] 資料庫檔案已保留: {db_filename}")