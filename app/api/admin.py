from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional
import datetime

from app.db.session import get_db, engine
from app.models.job_log import JobLog
from app.models.config import SystemConfig
from app.models.booster import BoosterConfig

# Import hàm ETL (lưu ý tên file import phải đúng với file bạn đang có)
# Nếu file của bạn là etl_from_oracle.py thì giữ nguyên dòng dưới
from etl_from_oracle import sync_from_oracle_fixed

router = APIRouter()

# --- MODELS (Khuôn mẫu dữ liệu) ---
class ConfigUpdate(BaseModel):
    key: str
    value: str

class BoosterUpdate(BaseModel):
    id: int
    booster_name: str
    coin_cost: int

class BoosterCreate(BaseModel):
    booster_key: str
    booster_name: str
    coin_cost: int

# --- API 1: LẤY LOGS ---
@router.get("/logs")
def get_logs(limit: int = 20, db: Session = Depends(get_db)):
    logs = db.query(JobLog).order_by(JobLog.start_time.desc()).limit(limit).all()
    return {"data": logs}

# --- API 2: CHẠY ETL THỦ CÔNG ---
@router.post("/run-etl")
def run_etl_manual(background_tasks: BackgroundTasks):
    # Chạy ngầm để không bị treo giao diện
    background_tasks.add_task(sync_from_oracle_fixed)
    return {"message": "Đã kích hoạt tiến trình đồng bộ dữ liệu!"}

# --- API 3: LẤY SYSTEM CONFIG ---
@router.get("/configs")
def get_configs(db: Session = Depends(get_db)):
    configs = db.query(SystemConfig).order_by(SystemConfig.key).all()
    return {"data": configs}

# --- API 4: CẬP NHẬT SYSTEM CONFIG ---
@router.post("/configs")
def update_config(config: ConfigUpdate, db: Session = Depends(get_db)):
    item = db.query(SystemConfig).filter(SystemConfig.key == config.key).first()
    if not item:
        # Nếu chưa có thì tạo mới
        item = SystemConfig(key=config.key, value=config.value)
        db.add(item)
    else:
        item.value = config.value
    
    db.commit()
    return {"message": "Cập nhật thành công"}

# --- API 5: LẤY DANH SÁCH BOOSTER ---
@router.get("/boosters")
def get_boosters(db: Session = Depends(get_db)):
    # Sắp xếp theo ID cho dễ nhìn
    boosters = db.query(BoosterConfig).order_by(BoosterConfig.id).all()
    return {"data": boosters}

# --- API 6: CẬP NHẬT BOOSTER (SỬA TÊN/GIÁ) ---
@router.post("/boosters")
def update_booster(booster: BoosterUpdate, db: Session = Depends(get_db)):
    item = db.query(BoosterConfig).filter(BoosterConfig.id == booster.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Booster not found")
    
    item.booster_name = booster.booster_name
    item.coin_cost = booster.coin_cost
    db.commit()
    return {"message": "Đã cập nhật Booster thành công!"}

# --- API 7: THÊM BOOSTER MỚI (CREATE) ---
@router.post("/boosters/new")
def create_booster(booster: BoosterCreate, db: Session = Depends(get_db)):
    # Kiểm tra trùng key
    exists = db.query(BoosterConfig).filter(BoosterConfig.booster_key == booster.booster_key).first()
    if exists:
        raise HTTPException(status_code=400, detail="Mã (Key) này đã tồn tại!")
    
    new_item = BoosterConfig(
        booster_key=booster.booster_key,
        booster_name=booster.booster_name,
        coin_cost=booster.coin_cost
    )
    db.add(new_item)
    db.commit()
    return {"message": "Thêm mới thành công!"}

# --- API 8: XÓA BOOSTER (DELETE) ---
@router.delete("/boosters/{id}")
def delete_booster(id: int, db: Session = Depends(get_db)):
    item = db.query(BoosterConfig).filter(BoosterConfig.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy Item")
    
    db.delete(item)
    db.commit()
    return {"message": "Đã xóa thành công!"}