from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # Tên Game (VD: Empire Defender)
    bundle_id = Column(String, unique=True, index=True) # ID trên Store (VD: com.zitga.empire)
    platform = Column(String)                       # iOS / Android
    
    # Các Key AppMetrica (để kéo data)
    appmetrica_app_id = Column(String, nullable=False)
    appmetrica_api_key = Column(String, nullable=False) # Token truy cập

    is_active = Column(Boolean, default=True)       # Game còn chạy không?
    created_at = Column(DateTime(timezone=True), server_default=func.now())