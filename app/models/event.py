from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class RawEvent(Base):
    __tablename__ = "raw_events"

    id = Column(Integer, primary_key=True, index=True)
    
    # Liên kết với bảng Games để biết event này của game nào
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    
    event_name = Column(String, index=True)        # Tên sự kiện (VD: level_start)
    event_timestamp = Column(DateTime, index=True) # Thời gian xảy ra event
    
    # Quan trọng: Lưu toàn bộ tham số event (level, difficulty...) vào cột JSON
    # Giúp linh hoạt, không cần sửa cấu trúc bảng khi Game thay đổi logic
    event_json = Column(JSON) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Thời gian kéo về DB