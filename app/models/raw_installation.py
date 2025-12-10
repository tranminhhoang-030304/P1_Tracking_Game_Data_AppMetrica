from sqlalchemy import Column, String, DateTime, BigInteger, Integer
from app.db.base import Base  # Hãy sửa lại đường dẫn import Base nếu cấu trúc bạn khác

class RawInstallation(Base):
    __tablename__ = "raw_installations"

    id = Column(Integer, primary_key=True, index=True)
    install_datetime = Column(DateTime, nullable=False)
    google_aid = Column(String, nullable=True)
    device_manufacturer = Column(String, nullable=True)
    appmetrica_device_id = Column(String, nullable=True) # ID thiết bị rất dài, phải dùng BigInteger
    os_name = Column(String, nullable=True)
    os_version = Column(String, nullable=True)