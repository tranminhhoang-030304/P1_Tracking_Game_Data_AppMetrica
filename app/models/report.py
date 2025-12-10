from sqlalchemy import Column, Integer, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProcessedReport(Base):
    __tablename__ = "processed_reports"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    
    date = Column(Date, index=True, nullable=False) # Ngày báo cáo (VD: 2025-12-08)
    
    # Các chỉ số quan trọng (KPIs)
    dau = Column(Integer, default=0)         # Daily Active Users
    revenue = Column(Float, default=0.0)     # Doanh thu trong ngày
    new_users = Column(Integer, default=0)   # User mới (NRU)
    
    # Ràng buộc: Mỗi game trong 1 ngày chỉ có 1 dòng báo cáo duy nhất
    __table_args__ = (
        UniqueConstraint('game_id', 'date', name='uix_game_date'),
    )