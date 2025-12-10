import oracledb
import json

# Cấu hình kết nối Oracle
ORACLE_USER = "skw_id"
ORACLE_PASS = "SKW#2021"
ORACLE_DSN = "103.147.34.20:1521/orclxtel"

def peek_event_json():
    print("🔍 Đang soi nội dung JSON của event 'Win_Battle'...")
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=ORACLE_DSN)
        cursor = conn.cursor()
        
        # Lấy 1 dòng Win_Battle
        sql = "SELECT EVENT_JSON FROM APPMETRICA_EVENTS_RAW WHERE EVENT_NAME = 'Win_Battle' FETCH FIRST 1 ROWS ONLY"
        cursor.execute(sql)
        row = cursor.fetchone()
        
        if row:
            lob_object = row[0]
            
            # --- SỬA LỖI Ở ĐÂY ---
            # Nếu dữ liệu là LOB (cái hộp), phải đọc nó ra thành chuỗi (String)
            if lob_object and hasattr(lob_object, 'read'):
                json_str = lob_object.read()
            else:
                json_str = str(lob_object) # Trường hợp nó đã là string sẵn
            
            # Giờ mới parse JSON
            parsed = json.loads(json_str)
            print("\n✅ TÌM THẤY CẤU TRÚC JSON (Copy đoạn dưới này gửi tôi nhé):")
            print("--------------------------------------------------")
            print(json.dumps(parsed, indent=4))
            print("--------------------------------------------------")
        else:
            print("⚠️ Không tìm thấy dòng Win_Battle nào.")
            
        conn.close()
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    peek_event_json()