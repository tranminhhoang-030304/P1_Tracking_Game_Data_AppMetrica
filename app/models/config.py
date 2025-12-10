from sqlalchemy import Column, String, Text
from app.db.base import Base

class SystemConfig(Base):
    __tablename__ = "system_configs"

    key = Column(String, primary_key=True, index=True) # Ví dụ: "ORACLE_HOST"
    value = Column(Text)                               # Ví dụ: "103.147.34.20"
    description = Column(String, nullable=True)