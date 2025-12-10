import requests

# --- CẤU HÌNH ---
APP_ID = '4781656'
TOKEN = 'y0__xD5h6-nCBimjTwgt8OAxBXQT7e05W7A8Otb5pV7SiISEYaFAg'
# Lưu ý: URL này chuẩn theo tài liệu mới nhất
URL = 'https://api.appmetrica.yandex.com/logs/v1/export/installations.csv'

headers = {
    'Authorization': f'OAuth {TOKEN}'
}

# Chỉ lấy đúng 1 trường đơn giản nhất để test kết nối
params = {
    'application_id': APP_ID,
    'date_since': '2024-12-01 00:00:00',
    'date_until': '2024-12-01 23:59:59',
    'fields': 'install_datetime', 
}

print(f"--- ĐANG KIỂM TRA KẾT NỐI ĐẾN APP ID: {APP_ID} ---")
print(f"URL: {URL}")

try:
    response = requests.get(URL, params=params, headers=headers)
    
    print(f"\n👉 HTTP STATUS CODE: {response.status_code}")
    print("\n👉 NỘI DUNG PHẢN HỒI TỪ SERVER (Đọc kỹ dòng dưới):")
    print("-" * 50)
    print(response.text) # In ra nguyên văn lỗi
    print("-" * 50)

except Exception as e:
    print(f"Lỗi Python: {e}")