# 檔案名稱: server/main.py
import socket
import threading
import json
import sys
import os

# 嘗試加入專案根目錄，以便 import 其他模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.db_engine import SteadyHandDB
from server.protocol import SteadyHandProtocol, CMD_UPLOAD_SCORE, CMD_GET_LEADERBOARD, CMD_ERROR

# [新增] 伺服器端簡易 .env 讀取器 (為了不依賴 steadyhand 套件)
def load_server_env(filepath=".env"):
    config = {"HOST": "0.0.0.0", "PORT": "9999"} # 預設值
    if os.path.exists(filepath):
        print(f"[Server] Loading config from {filepath}")
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    # 我們只關心 PORT，HOST 通常固定 0.0.0.0
                    if k.strip() == "SERVER_PORT":
                        config["PORT"] = v.strip()
    return config

# 載入設定
env_config = load_server_env()
HOST = "0.0.0.0" # Server 永遠監聽所有介面
PORT = int(env_config["PORT"])
DB_FILE = "steadyhand.db"

class SteadyHandServer:
    def __init__(self):
        self.db = SteadyHandDB(DB_FILE)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        print(f"[Server] Listening on {HOST}:{PORT}")

    def start(self):
        try:
            while True:
                client_sock, addr = self.server_socket.accept()
                print(f"[Server] New connection from {addr}")
                client_handler = threading.Thread(
                    target=self.handle_client,
                    args=(client_sock,)
                )
                client_handler.start()
        except KeyboardInterrupt:
            print("[Server] Shutting down...")
        finally:
            self.server_socket.close()

    def recv_all(self, sock, count):
        buf = b''
        while len(buf) < count:
            try:
                newbuf = sock.recv(count - len(buf))
                if not newbuf: return None
                buf += newbuf
            except:
                return None
        return buf

    def handle_client(self, conn):
        try:
            while True:
                header_data = self.recv_all(conn, SteadyHandProtocol.HEADER_SIZE)
                if not header_data: break
                
                cmd, length = SteadyHandProtocol.unpack_header(header_data)
                body_data = self.recv_all(conn, length)
                if not body_data: break
                
                try:
                    payload = json.loads(body_data.decode('utf-8'))
                except json.JSONDecodeError:
                    print("[Server] JSON Decode Error")
                    continue

                response_payload = {}
                
                if cmd == CMD_UPLOAD_SCORE:
                    user = payload.get("user", "Unknown")
                    lvl = payload.get("level", 1)
                    time_val = payload.get("time", 999.0)
                    stars = payload.get("stars", 0)
                    self.db.add_score(user, lvl, time_val, stars)
                    response_payload = {"status": "ok", "msg": "Score saved"}
                    print(f"[Server] Saved score for {user}")

                elif cmd == CMD_GET_LEADERBOARD:
                    lvl = payload.get("level", 1)
                    top_scores = self.db.get_leaderboard(lvl)
                    response_payload = {"status": "ok", "data": top_scores}
                    print(f"[Server] Sent leaderboard for Lv.{lvl}")

                else:
                    response_payload = {"status": "error", "msg": "Unknown CMD"}

                resp_packet = SteadyHandProtocol.pack_packet(cmd, response_payload)
                conn.sendall(resp_packet)
                break 

        except Exception as e:
            print(f"[Server] Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    server = SteadyHandServer()
    server.start()