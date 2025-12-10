from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.booster import BoosterConfig

def init_boosters():
    print("🎮 Đang khởi tạo dữ liệu Booster mẫu...")
    session = Session(engine)
    
    # Dữ liệu mẫu để demo cho sếp
    data = [
        {"key": "booster_hammer", "name": "Búa Thần (Hammer)", "cost": 100},
        {"key": "booster_magnet", "name": "Nam Châm Hút", "cost": 150},
        {"key": "booster_bomb", "name": "Bom Nổ Chậm", "cost": 200},
        {"key": "booster_move", "name": "Thêm 5 Lượt", "cost": 50},
        {"key": "booster_refresh", "name": "Đổi Màu (Refresh)", "cost": 80},
    ]
    
    count = 0
    for item in data:
        # Kiểm tra xem đã có chưa, chưa có mới thêm
        exists = session.query(BoosterConfig).filter_by(booster_key=item["key"]).first()
        if not exists:
            new_b = BoosterConfig(
                booster_key=item["key"], 
                booster_name=item["name"], 
                coin_cost=item["cost"]
            )
            session.add(new_b)
            count += 1
    
    session.commit()
    session.close()
    
    if count > 0:
        print(f"✅ Đã thêm mới {count} loại Booster vào hệ thống!")
    else:
        print("ℹ️ Dữ liệu Booster đã có sẵn, không cần thêm.")

if __name__ == "__main__":
    init_boosters()