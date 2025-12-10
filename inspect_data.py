import pandas as pd
import os

# --- CẤU HÌNH TÊN FILE (Khớp với code extractor mới nhất) ---
DATE_FROM = "2025-11-01"
DATE_TO = "2025-12-08"

FILE_INSTALLS = f"raw_installations_{DATE_FROM}_to_{DATE_TO}.csv"
FILE_CLICKS = f"raw_clicks_{DATE_FROM}_to_{DATE_TO}.csv"

def inspect_file(filename):
    print(f"\n{'='*20} KIỂM TRA FILE: {filename} {'='*20}")
    
    if not os.path.exists(filename):
        print(f"❌ Không tìm thấy file: {filename}")
        print("👉 Gợi ý: Bạn hãy nhìn vào thư mục xem tên file thực tế là gì, có thể ngày kết thúc khác 2025-12-08?")
        return

    try:
        # Đọc file CSV
        df = pd.read_csv(filename)
        
        # 1. Kiểm tra kích thước
        row_count = df.shape[0]
        print(f"📊 Kích thước: {row_count} dòng, {df.shape[1]} cột")
        
        if row_count > 0:
            # 2. Xem mẫu dữ liệu nếu có dữ liệu
            print(f"📋 Danh sách cột: {list(df.columns)}")
            print("\n👀 Dữ liệu mẫu (3 dòng đầu):")
            print(df.head(3))
            print("\nℹ️ Kiểu dữ liệu:")
            print(df.dtypes)
            print("\n✅ KẾT LUẬN: File ngon lành, sẵn sàng nạp vào Database!")
        else:
            print("⚠️ CẢNH BÁO: File vẫn rỗng (0 dòng). Hãy kiểm tra lại Dashboard xem traffic rơi vào ngày nào.")
        
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")

# Chạy kiểm tra
if __name__ == "__main__":
    inspect_file(FILE_INSTALLS)
    inspect_file(FILE_CLICKS)