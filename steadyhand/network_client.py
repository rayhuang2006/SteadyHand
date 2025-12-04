# 檔案名稱: steadyhand/network_client.py
import socket
import json
import threading
import os
import uuid
import struct

# 通訊協定定義 (必須與 Server 保持一致)
CMD_UPLOAD_SCORE = 1
CMD_GET_LEADERBOARD = 2
HEADER_FORMAT = ">BI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

class NetworkClient:
    def __init__(self, host='127.0.0.1', port=9999):
        self.server_addr = (host, port)
        # 取得或建立使用者 ID
        self.user_id = self.get_or_create_user_id()
        # 簡單產生一個代號名字，未來可以做改名功能
        self.username = f"Player-{self.user_id[:4]}"
        
        # 排行榜快取: { level_id: [records...] }
        self.leaderboard_cache = {} 
        self.is_loading = False

    def get_or_create_user_id(self):
        """讀取本地 user_id.txt，若無則生成新的 UUID"""
        id_file = "user_id.txt"
        if os.path.exists(id_file):
            with open(id_file, "r") as f:
                return f.read().strip()
        else:
            new_id = str(uuid.uuid4())
            with open(id_file, "w") as f:
                f.write(new_id)
            return new_id

    def _send_request(self, cmd, payload):
        """(內部函式) 建立連線 -> 發送 -> 接收 -> 斷線"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3.0) # 設定 3 秒逾時，避免卡死
            sock.connect(self.server_addr)
            
            # 1. 打包請求
            payload_bytes = json.dumps(payload).encode('utf-8')
            header = struct.pack(HEADER_FORMAT, cmd, len(payload_bytes))
            sock.sendall(header + payload_bytes)
            
            # 2. 接收檔頭 (Header)
            resp_header = sock.recv(HEADER_SIZE)
            if not resp_header: return None
            r_cmd, r_len = struct.unpack(HEADER_FORMAT, resp_header)
            
            # 3. 接收內容 (Body)
            # 簡單實作：假設一次 recv 就能讀完 JSON (對於排行榜通常足夠)
            resp_body = sock.recv(r_len)
            response = json.loads(resp_body.decode('utf-8'))
            
            sock.close()
            return response
        except Exception as e:
            print(f"[Network] Error: {e}")
            return None

    def upload_score_async(self, level, time_spent, stars):
        """[非同步] 上傳成績"""
        def task():
            print(f"[Network] Uploading score for Lv.{level}...")
            data = {
                "user": self.username,
                "level": level,
                "time": time_spent,
                "stars": stars
            }
            res = self._send_request(CMD_UPLOAD_SCORE, data)
            
            if res and res.get("status") == "ok":
                print("[Network] Upload success!")
                
                # [關鍵修正] 上傳成功後，清除該關卡的快取
                # 這樣下次顯示排行榜時，會強制重新下載，就能看到剛上傳的成績
                if level in self.leaderboard_cache:
                    del self.leaderboard_cache[level]
            else:
                print("[Network] Upload failed.")
        
        threading.Thread(target=task).start()

    def fetch_leaderboard_async(self, level):
        """[非同步] 下載排行榜"""
        def task():
            self.is_loading = True
            # print(f"[Network] Fetching leaderboard for Lv.{level}...")
            data = {"level": level}
            res = self._send_request(CMD_GET_LEADERBOARD, data)
            
            if res and res.get("status") == "ok":
                self.leaderboard_cache[level] = res["data"]
                # print(f"[Network] Leaderboard Lv.{level} updated.")
            
            self.is_loading = False
        
        # 啟動背景執行緒
        threading.Thread(target=task).start()

    def get_cached_leaderboard(self, level):
        """取得目前快取的排行榜 (不會卡頓)"""
        return self.leaderboard_cache.get(level, [])