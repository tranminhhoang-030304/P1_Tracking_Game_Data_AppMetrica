from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class BoosterConfig(Base):
    __tablename__ = "booster_configs"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, index=True)
    booster_key = Column(String, unique=True, index=True)
    booster_name = Column(String)
    coin_cost = Column(Integer, default=0)
    description = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# --- QUAN TRỌNG: Dòng này giúp code cũ (Booster) và mới (BoosterConfig) đều chạy được ---
Booster = BoosterConfig