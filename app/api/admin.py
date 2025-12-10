from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List

from app.db.session import engine
from app.models.job_log import JobLog
from app.models.config import SystemConfig
# Import hàm ETL để nút bấm có thể gọi
from etl_from_oracle import sync_from_oracle_fixed

router = APIRouter()

def get_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- MODEL DỮ LIỆU (Pydantic) ---
class ConfigUpdate(BaseModel):
    key: str
    value: str

# --- API 1: LẤY LỊCH SỬ CHẠY (MONITOR) ---
@router.get("/logs")
def get_job_logs(limit: int = 20, db: Session = Depends(get_db)):
    logs = db.query(JobLog).order_by(desc(JobLog.start_time)).limit(limit).all()
    return {"data": logs}

# --- API 2: LẤY CẤU HÌNH (SETTINGS) ---
@router.get("/configs")
def get_configs(db: Session = Depends(get_db)):
    configs = db.query(SystemConfig).all()
    return {"data": configs}

# --- API 3: CẬP NHẬT CẤU HÌNH ---
@router.post("/configs")
def update_config(config: ConfigUpdate, db: Session = Depends(get_db)):
    item = db.query(SystemConfig).filter(SystemConfig.key == config.key).first()
    if not item:
        raise HTTPException(status_code=404, detail="Config key not found")
    
    item.value = config.value
    db.commit()
    return {"message": "Update success"}

# --- API 4: KÍCH HOẠT CHẠY ETL NGAY (RUN NOW) ---
@router.post("/run-etl")
def trigger_etl_job(background_tasks: BackgroundTasks):
    # Chạy ngầm (Background) để không làm treo Web
    background_tasks.add_task(sync_from_oracle_fixed)
    return {"message": "Đã gửi lệnh chạy ETL! Vui lòng chờ và theo dõi tại tab Monitor."}