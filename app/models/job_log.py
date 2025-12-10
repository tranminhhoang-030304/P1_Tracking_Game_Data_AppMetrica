from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class JobLog(Base):
    __tablename__ = "job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, index=True) # Ví dụ: "ETL Oracle Sync"
    status = Column(String)               # "SUCCESS", "FAILED", "RUNNING"
    rows_imported = Column(Integer, default=0)
    message = Column(Text, nullable=True) # Ghi chú lỗi hoặc chi tiết
    
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)