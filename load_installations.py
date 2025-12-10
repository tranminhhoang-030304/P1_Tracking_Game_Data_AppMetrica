import pandas as pd
import sys
import os

sys.path.append(os.getcwd())

from app.db.session import SessionLocal, engine
from app.models.raw_installation import RawInstallation
from app.db.base import Base
from sqlalchemy import text # Import thêm để xử lý lỗi

# Nhớ kiểm tra lại tên file CSV cho đúng với file bạn đang có
CSV_FILE = "raw_installations_2025-11-01_to_2025-12-08.csv"

def load_csv_to_db():
    print(f"🚀 Bắt đầu nạp dữ liệu từ {CSV_FILE}...")
    
    # --- 1. XÓA BẢNG CŨ (Để cập nhật Schema mới là String) ---
    try:
        print("🗑️ Đang xóa bảng cũ để cập nhật cấu trúc mới...")
        RawInstallation.__table__.drop(engine)
    except Exception:
        print(" (Bảng chưa tồn tại hoặc không thể xóa, tiếp tục...)")

    # --- 2. TẠO LẠI BẢNG ---
    Base.metadata.create_all(bind=engine)
    
    # --- 3. ĐỌC DỮ LIỆU ---
    try:
        df = pd.read_csv(CSV_FILE)
        df['install_datetime'] = pd.to_datetime(df['install_datetime'])
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy file CSV. Kiểm tra lại tên file!")
        return

    # --- 4. GHI DỮ LIỆU ---
    db = SessionLocal()
    try:
        count = 0
        total = len(df)
        batch = []
        
        for index, row in df.iterrows():
            install_obj = RawInstallation(
                install_datetime=row['install_datetime'],
                google_aid=row['google_aid'] if pd.notna(row['google_aid']) else None,
                device_manufacturer=row['device_manufacturer'],
                
                # Ép kiểu về String để khớp với Model mới
                appmetrica_device_id=str(row['appmetrica_device_id']), 
                
                os_name=row['os_name'],
                os_version=str(row['os_version'])
            )
            batch.append(install_obj)
            
            if len(batch) >= 1000:
                db.add_all(batch)
                db.commit()
                count += len(batch)
                print(f" -> Đã nạp {count}/{total} dòng...")
                batch = [] 
        
        if batch:
            db.add_all(batch)
            db.commit()
            count += len(batch)
            
        print(f"✅ HOÀN TẤT! Tổng cộng đã nạp {count} dòng vào Database.")
        
    except Exception as e:
        print(f"❌ Lỗi khi ghi Database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_csv_to_db()