import requests
import time
import os

# --- 1. CẤU HÌNH KẾT NỐI ---
APP_ID = '4781656'
TOKEN = 'y0__xD5h6-nCBimjTwgt8OAxBXQT7e05W7A8Otb5pV7SiISEYaFAg'
BASE_URL = 'https://api.appmetrica.yandex.com/logs/v1/export'

HEADERS = {
    'Authorization': f'OAuth {TOKEN}'
}

# --- 2. CẤU HÌNH TRƯỜNG DỮ LIỆU ---
DATA_CONFIG = {
    "installations": [
        "install_datetime", 
        "google_aid", 
        "device_manufacturer",
        "appmetrica_device_id",
        "os_name",
        "os_version"
    ],
    "clicks": [
        "click_datetime", 
        "click_id",
        "google_aid"
    ]
}

# --- 3. HÀM TẢI DỮ LIỆU BỀN BỈ (CORE LOGIC) ---
def download_data_persistent(source, fields, date_from, date_to):
    # Tạo URL file .csv
    url = f"{BASE_URL}/{source}.csv"
    
    # Tham số
    params = {
        'application_id': APP_ID,
        'date_since': f'{date_from} 00:00:00',
        'date_until': f'{date_to} 23:59:59',
        'fields': ','.join(fields)
    }
    
    filename = f"raw_{source}_{date_from}_to_{date_to}.csv"
    print(f"\n--- BẮT ĐẦU TẢI: {source.upper()} ---")
    
    retry_count = 0
    max_retries = 20 # Thử tối đa 20 lần
    
    while retry_count < max_retries:
        try:
            print(f"[{retry_count+1}] Đang gửi yêu cầu lấy dữ liệu...", end=' ')
            
            # Gửi request
            response = requests.get(url, params=params, headers=HEADERS, stream=True)
            
            # TRƯỜNG HỢP 1: THÀNH CÔNG (200) -> Tải file luôn
            if response.status_code == 200:
                print("\n✅ DỮ LIỆU ĐÃ SẴN SÀNG! Đang ghi xuống đĩa...")
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192): 
                        f.write(chunk)
                print(f" -> Hoàn tất: {os.path.abspath(filename)}")
                return True
            
            # TRƯỜNG HỢP 2: ĐANG XỬ LÝ (202) -> Đợi
            elif response.status_code == 202:
                print("⏳ (Server đang nén file... Đợi 30s)")
                time.sleep(30) # Đợi 30 giây rồi hỏi lại
                retry_count += 1
            
            # TRƯỜNG HỢP 3: LỖI KHÁC
            else:
                print(f"\n❌ LỖI: Code {response.status_code}")
                print(f"Chi tiết: {response.text[:100]}...")
                return False
                
        except Exception as e:
            print(f"\n❌ Lỗi kết nối mạng: {e}")
            time.sleep(10)
            retry_count += 1

    print("\n⚠️ Quá thời gian chờ (Timeout). Hãy thử lại sau.")
    return False

# --- 4. CHẠY CHƯƠNG TRÌNH (MAIN) ---
if __name__ == "__main__":
    # Cập nhật thời gian chính xác theo dữ liệu thật của App (Năm 2025)
    DATE_FROM = "2025-11-01" 
    DATE_TO = "2025-12-08" 

    print(f"📡 ĐANG KẾT NỐI ĐẾN APP ID: {APP_ID}")
    print(f"📅 KHOẢNG THỜI GIAN: {DATE_FROM} đến {DATE_TO} (Năm 2025)\n")

    for source_type, fields_list in DATA_CONFIG.items():
        download_data_persistent(source_type, fields_list, DATE_FROM, DATE_TO)