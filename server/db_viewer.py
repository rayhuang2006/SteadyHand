# 檔案名稱: server/db_viewer.py
import struct
import os
import time

def view_database(db_file="steadyhand.db"):
    if not os.path.exists(db_file):
        print(f"錯誤: 找不到資料庫檔案 {db_file}")
        return

    # 必須與 db_engine.py 使用完全相同的格式
    fmt = "16sIfId"
    record_size = struct.calcsize(fmt)
    
    print(f"{'USER':<16} | {'LV':<3} | {'TIME':<8} | {'STARS':<5} | {'DATE'}")
    print("-" * 65)

    with open(db_file, "rb") as f:
        count = 0
        while True:
            chunk = f.read(record_size)
            if not chunk:
                break
            
            try:
                # 解包二進位數據
                name_b, lvl, t, stars, ts = struct.unpack(fmt, chunk)
                
                # 清理數據 (去除 \x00)
                name = name_b.decode('utf-8').rstrip('\x00')
                date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
                
                print(f"{name:<16} | {lvl:<3} | {t:<8.2f} | {stars:<5} | {date_str}")
                count += 1
            except struct.error:
                print("[Error] 讀取到損壞的數據區塊")

    print("-" * 65)
    print(f"總計: {count} 筆資料")

if __name__ == "__main__":
    view_database()