from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class LevelSessionFact(Base):
    """
    Bảng này lưu kết quả sau khi đã xử lý dữ liệu thô từ AppMetrica.
    Mỗi dòng là 1 lượt chơi (Session) của 1 user tại 1 level.
    """
    __tablename__ = "fact_level_sessions"

    session_id = Column(String, primary_key=True, index=True) # Session ID từ AppMetrica
    user_id = Column(String, index=True)      # appmetrica_device_id
    game_id = Column(String, index=True)
    
    level_id = Column(Integer, index=True)
    status = Column(String)                   # 'WIN' hoặc 'FAIL'
    
    # Các chỉ số quan trọng (Metrics)
    total_coin_spent = Column(Integer, default=0)    # Tổng tiền tiêu trong màn
    total_boosters_used = Column(Integer, default=0) # Tổng số booster dùng
    play_time_seconds = Column(Integer, default=0)   # Thời gian chơi
    
    event_timestamp = Column(DateTime)               # Thời gian xảy ra sự kiện
    processed_at = Column(DateTime(timezone=True), server_default=func.now())