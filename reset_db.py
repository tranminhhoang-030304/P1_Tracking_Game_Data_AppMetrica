from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base
# Import các models để tạo lại bảng sau khi xóa
from app.models import job_log, config, analytics, booster

def reset_database():
    print("⚠️  CẢNH BÁO: Đang xóa Database với chế độ CASCADE (Bất chấp ràng buộc)...")
    
    # Sử dụng engine.begin() để tự động commit transaction
    with engine.begin() as conn:
        # 1. Danh sách các bảng cần xóa (Bao gồm cả bảng cũ gây lỗi)
        # Thứ tự không quan trọng vì ta sẽ dùng CASCADE
        tables_to_drop = [
            "boosters", 
            "games", 
            "fact_level_sessions", 
            "job_logs", 
            "system_configs", 
            "booster_configs",
            "alembic_version" # Xóa cả lịch sử migration nếu có
        ]
        
        for table in tables_to_drop:
            try:
                # Lệnh CASCADE: Xóa bảng này và tất cả những gì liên quan đến nó
                conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                print(f"   🗑️  Đã xóa bảng: {table}")
            except Exception as e:
                print(f"   ⚠️  Không xóa được {table} (Có thể chưa tồn tại): {e}")

    # 2. Tạo lại bảng mới tinh
    print("✨  Đang tạo lại cấu trúc bảng mới...")
    Base.metadata.create_all(bind=engine)
    print("✅  DATABASE ĐÃ ĐƯỢC LÀM SẠCH HOÀN TOÀN!")

if __name__ == "__main__":
    reset_database()