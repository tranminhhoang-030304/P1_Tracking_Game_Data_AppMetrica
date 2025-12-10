import json
import time
import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.analytics import LevelSessionFact
from app.models.booster import BoosterConfig

# === 🔴 CẤU HÌNH (HÃY ĐỐI CHIẾU VỚI JAVA VÀ SỬA Ở ĐÂY) ===
APP_ID = "4781656" 
TOKEN = "y0__xD5h6-nCBimjTwgt8OAxBXQT7e05W7A8Otb5pV7SiISEYaFAg"
# Thử bỏ trống event_name_include để xem Server có những loại event gì?
# Nếu Java dùng tên khác, bạn hãy điền vào đây.
EVENT_NAMES_FILTER = "missionComplete,missionFail" 
DATE_SINCE = "2024-01-01" # Thử lấy 1 năm gần nhất

def fetch_and_debug_api():
    base_url = "https://api.appmetrica.yandex.com/logs/v1/export/events.json"
    params = {
        "application_id": APP_ID,
        "date_since": DATE_SINCE,
        "date_until": datetime.now().strftime('%Y-%m-%d'),
        "fields": "event_name,event_json,appmetrica_device_id,session_id,event_timestamp",
    }
    
    # Nếu biết chắc tên event thì lọc, không thì bỏ dòng này để xem tất cả
    if EVENT_NAMES_FILTER:
        params["event_name_include"] = EVENT_NAMES_FILTER
        
    headers = {"Authorization": f"OAuth {TOKEN}"}

    print(f"🚀 Bắt đầu gọi API với AppID={APP_ID} từ ngày {DATE_SINCE}...")

    # Cơ chế Retry Check File (Giống module Java của sếp)
    max_retries = 30
    sleep_time = 30 # Đợi 30s mỗi lần (API xuất file lớn cần đợi lâu)

    for attempt in range(max_retries):
        print(f"   ⏳ [Lần {attempt+1}/{max_retries}] Đang kiểm tra trạng thái file...")
        try:
            response = requests.get(base_url, params=params, headers=headers, stream=True)
            
            if response.status_code == 200:
                print("   ✅ File đã sẵn sàng! Đang tải xuống và phân tích...")
                
                count = 0
                sample_events = set()
                
                # Stream dữ liệu để không bị tràn RAM
                for line in response.iter_lines():
                    if line:
                        try:
                            event = json.loads(line.decode('utf-8'))
                            count += 1
                            # Thu thập tên các event để debug
                            sample_events.add(event.get('event_name'))
                            
                            # --- ĐOẠN NÀY GỌI HÀM XỬ LÝ (TÍNH COIN) ---
                            # process_single_event(event) 
                        except:
                            continue
                
                print(f"   📥 Tổng cộng đã tải: {count} sự kiện.")
                print(f"   🔍 Các loại Event tìm thấy trong dữ liệu: {sample_events}")
                
                if count == 0:
                    print("   ⚠️ Cảnh báo: Kết nối OK nhưng không có dòng dữ liệu nào.")
                    print("   👉 GỢI Ý: Hãy kiểm tra lại 'date_since' hoặc 'event_name_include'.")
                
                return # Thành công thì thoát

            elif response.status_code == 202:
                print(f"   💤 Server đang xuất file (Processing). Đợi {sleep_time}s nữa...")
                time.sleep(sleep_time)
            
            else:
                print(f"   ❌ Lỗi: {response.status_code} - {response.text}")
                return

        except Exception as e:
            print(f"   ❌ Lỗi kết nối: {e}")
            time.sleep(sleep_time)

if __name__ == "__main__":
    fetch_and_debug_api()