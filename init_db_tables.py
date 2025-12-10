# init_db_tables.py
from app.db.base import Base
from app.db.session import engine

# QUAN TRỌNG: Phải import đầy đủ TẤT CẢ các models cần tạo bảng ở đây
from app.models.booster import BoosterConfig
from app.models.analytics import LevelSessionFact  # <-- Dòng này phải có để tạo bảng Analytics

def init_tables():
    print("🔄 Đang khởi tạo/cập nhật các bảng trong Database...")
    
    # Lệnh này sẽ quét các models đã import ở trên và tạo bảng nếu chưa có
    Base.metadata.create_all(bind=engine)
    print("✅ Đã tạo bảng thành công (bao gồm cả fact_level_sessions)!")
    
    # --- Phần thêm dữ liệu mẫu (Giữ nguyên) ---
    from sqlalchemy.orm import Session
    session = Session(engine)
    try:
        if session.query(BoosterConfig).count() == 0:
            print("➕ Đang thêm dữ liệu mẫu cho Booster Config...")
            # (Code thêm dữ liệu mẫu giữ nguyên như cũ...)
            sample_boosters = [
                BoosterConfig(game_id="4781656", booster_key="booster_Hammer", coin_cost=100, booster_name="Hammer"),
                BoosterConfig(game_id="4781656", booster_key="booster_Magnet", coin_cost=50, booster_name="Magnet"),
                BoosterConfig(game_id="4781656", booster_key="booster_Add", coin_cost=80, booster_name="Add Moves"),
                BoosterConfig(game_id="4781656", booster_key="booster_Clear", coin_cost=120, booster_name="Clear Board"),
                BoosterConfig(game_id="4781656", booster_key="booster_Unlock", coin_cost=200, booster_name="Unlock Level"),
                BoosterConfig(game_id="4781656", booster_key="revive_boosterClear", coin_cost=150, booster_name="Revive")
            ]
            session.add_all(sample_boosters)
            session.commit()
            print("✅ Đã thêm dữ liệu mẫu thành công!")
    except Exception as e:
        print(f"ℹ️ Thông báo DB: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_tables()