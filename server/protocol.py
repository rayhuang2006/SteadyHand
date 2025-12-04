# 檔案名稱: server/protocol.py
import struct
import json

# --- 協定常數定義 ---
CMD_UPLOAD_SCORE = 1
CMD_GET_LEADERBOARD = 2
CMD_ERROR = 255

class SteadyHandProtocol:
    """
    SHP (SteadyHand Protocol) 封包處理器
    格式: [CMD(1B)] [LENGTH(4B)] [PAYLOAD(JSON)]
    """
    
    # Header 格式: 1 byte (unsigned char) + 4 bytes (unsigned int)
    # B: unsigned char (1 byte)
    # I: unsigned int (4 bytes)
    # >: Big Endian (網路傳輸標準位元組順序)
    HEADER_FORMAT = ">BI" 
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT) # 應該是 5 bytes

    @staticmethod
    def pack_packet(cmd_id: int, payload_dict: dict) -> bytes:
        """
        將指令與資料打包成二進位封包
        """
        # 1. 將字典轉成 JSON 字串，再轉成 bytes
        payload_json = json.dumps(payload_dict)
        payload_bytes = payload_json.encode('utf-8')
        
        # 2. 計算長度
        length = len(payload_bytes)
        
        # 3. 製作 Header
        header = struct.pack(SteadyHandProtocol.HEADER_FORMAT, cmd_id, length)
        
        # 4. 組合 (Header + Body)
        return header + payload_bytes

    @staticmethod
    def unpack_header(header_bytes: bytes):
        """
        解析 Header，回傳 (cmd_id, payload_length)
        """
        if len(header_bytes) != SteadyHandProtocol.HEADER_SIZE:
            return None, 0
        return struct.unpack(SteadyHandProtocol.HEADER_FORMAT, header_bytes)

# --- 自我測試 ---
if __name__ == "__main__":
    # 模擬 Client 打包資料
    test_data = {"user": "Ray", "time": 12.5}
    packet = SteadyHandProtocol.pack_packet(CMD_UPLOAD_SCORE, test_data)
    
    print(f"原始資料: {test_data}")
    print(f"打包後的 Bytes: {packet}")
    print(f"總長度: {len(packet)} bytes (Header 5 + Body {len(packet)-5})")
    
    # 模擬 Server 解析
    # 1. 先讀 Header (前 5 bytes)
    header_part = packet[:5]
    cmd, length = SteadyHandProtocol.unpack_header(header_part)
    print(f"解析 Header -> CMD: {cmd}, Length: {length}")
    
    # 2. 再讀 Body
    body_part = packet[5:5+length]
    restored_data = json.loads(body_part.decode('utf-8'))
    print(f"解析 Body -> {restored_data}")