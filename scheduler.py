import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.config import SystemConfig
# Import hàm ETL chuẩn (đảm bảo tên hàm khớp với file etl_from_oracle.py của bạn)
from etl_from_oracle import sync_from_oracle_fixed

def get_sleep_minutes():
    """
    Hàm đọc cấu hình từ Database.
    Nếu sếp sửa trên Web, hàm này sẽ lấy được giá trị mới ngay lập tức.
    """
    session = Session(engine)
    try:
        # Tìm config có key là CRON_SCHEDULE
        cfg = session.query(SystemConfig).filter_by(key="CRON_SCHEDULE").first()
        if cfg and cfg.value.isdigit():
            return int(cfg.value)
        return 30 # Mặc định 30 phút nếu không tìm thấy hoặc lỗi
    except Exception as e:
        print(f"⚠️ Lỗi đọc cấu hình: {e}. Dùng mặc định 30 phút.")
        return 30
    finally:
        session.close()

print("🚀 [Smart Scheduler] Đã khởi động! Sẵn sàng phục vụ theo lệnh Database.")

# Vòng lặp vĩnh cửu
while True:
    print(f"\n⏰ [Scheduler] Bắt đầu chạy Job lúc: {datetime.now()}")
    
    # 1. THỰC HIỆN CÔNG VIỆC
    try:
        sync_from_oracle_fixed()
        print("✅ [Scheduler] Job hoàn thành.")
    except Exception as e:
        print(f"❌ [Scheduler] Job gặp lỗi: {e}")

    # 2. ĐỌC CẤU HÌNH CHO LẦN TIẾP THEO
    minutes = get_sleep_minutes()
    
    # Bảo vệ: Không cho phép ngủ dưới 1 phút (tránh spam server)
    if minutes < 1: minutes = 1
    
    print(f"💤 Theo cấu hình, hệ thống sẽ nghỉ {minutes} phút...")
    
    # 3. NGỦ (Đếm giây)
    time.sleep(minutes * 60)
    