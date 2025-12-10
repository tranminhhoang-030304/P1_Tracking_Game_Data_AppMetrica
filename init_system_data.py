from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.config import SystemConfig

def init_default_configs():
    print("⚙️ Đang khởi tạo cấu hình hệ thống mặc định...")
    session = Session(engine)

    # Danh sách cấu hình mặc định (Lấy từ code cũ của bạn)
    default_configs = [
        {"key": "ORACLE_USER", "value": "skw_id", "description": "Tên đăng nhập Oracle"},
        {"key": "ORACLE_PASS", "value": "SKW#2021", "description": "Mật khẩu Oracle"},
        {"key": "ORACLE_HOST", "value": "103.147.34.20", "description": "Địa chỉ IP máy chủ Oracle"},
        {"key": "ORACLE_PORT", "value": "1521", "description": "Cổng kết nối Oracle"},
        {"key": "ORACLE_SERVICE", "value": "orclxtel", "description": "Tên dịch vụ (SID/Service Name)"},
        {"key": "APP_ID", "value": "4769050", "description": "AppMetrica Application ID"},
        {"key": "CRON_SCHEDULE", "value": "30", "description": "Chu kỳ chạy tự động (phút)"}
    ]

    count = 0
    for item in default_configs:
        # Kiểm tra xem config đã tồn tại chưa
        exists = session.query(SystemConfig).filter_by(key=item["key"]).first()
        if not exists:
            new_config = SystemConfig(
                key=item["key"],
                value=item["value"],
                description=item["description"]
            )
            session.add(new_config)
            count += 1
    
    session.commit()
    session.close()
    
    if count > 0:
        print(f"✅ Đã thêm mới {count} cấu hình vào Database.")
    else:
        print("ℹ️ Cấu hình đã tồn tại đầy đủ, không cần thêm.")

if __name__ == "__main__":
    init_default_configs()