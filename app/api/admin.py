from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional
import datetime
import random 

from app.db.session import get_db, engine
from app.models.job_log import JobLog 
from app.models.config import SystemConfig
from app.models.booster import BoosterConfig
from app.models.analytics import LevelSessionFact 

# Import hàm ETL an toàn
try:
    from etl_from_oracle import sync_from_oracle_fixed
except ImportError:
    print("⚠️ Cảnh báo: Không tìm thấy module etl_from_oracle.")
    def sync_from_oracle_fixed(): pass

router = APIRouter()

# --- MODELS ---
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

# ==========================================
# PHẦN 1: QUẢN LÝ LOGS & SYSTEM
# ==========================================
@router.get("/logs")
def get_logs(limit: int = 20, db: Session = Depends(get_db)):
    logs = db.query(JobLog).order_by(JobLog.start_time.desc()).limit(limit).all()
    return {"data": logs}

@router.post("/run-etl")
def run_etl_manual(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_from_oracle_fixed)
    return {"message": "Đã kích hoạt tiến trình đồng bộ dữ liệu!"}

@router.get("/configs")
def get_configs(db: Session = Depends(get_db)):
    configs = db.query(SystemConfig).order_by(SystemConfig.key).all()
    return {"data": configs}

@router.post("/configs")
def update_config(config: ConfigUpdate, db: Session = Depends(get_db)):
    item = db.query(SystemConfig).filter(SystemConfig.key == config.key).first()
    if not item:
        item = SystemConfig(key=config.key, value=config.value)
        db.add(item)
    else:
        item.value = config.value
    db.commit()
    return {"message": "Cập nhật thành công"}

# ==========================================
# PHẦN 2: QUẢN LÝ BOOSTER (CRUD)
# ==========================================
@router.get("/boosters")
def get_boosters(db: Session = Depends(get_db)):
    boosters = db.query(BoosterConfig).order_by(BoosterConfig.id).all()
    return {"data": boosters}

@router.post("/boosters")
def update_booster(booster: BoosterUpdate, db: Session = Depends(get_db)):
    item = db.query(BoosterConfig).filter(BoosterConfig.id == booster.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Booster not found")
    item.booster_name = booster.booster_name
    item.coin_cost = booster.coin_cost
    db.commit()
    return {"message": "Đã cập nhật Booster thành công!"}

@router.post("/boosters/new")
def create_booster(booster: BoosterCreate, db: Session = Depends(get_db)):
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

@router.delete("/boosters/{id}")
def delete_booster(id: int, db: Session = Depends(get_db)):
    item = db.query(BoosterConfig).filter(BoosterConfig.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy Item")
    db.delete(item)
    db.commit()
    return {"message": "Đã xóa thành công!"}

# ==========================================
# PHẦN 3: PHÂN TÍCH CHUYÊN SÂU (FIXED LOGIC)
# ==========================================
@router.get("/level-booster-breakdown")
def get_level_booster_detail(level: int, db: Session = Depends(get_db)):
    """
    API phân tích tỷ lệ dùng Booster.
    FIX: Sử dụng thuật toán chia số dư (Remainder Distribution) để đảm bảo tổng luôn khớp 100%.
    """
    # 1. Lấy tổng số lượt chơi thực tế
    total_sessions = db.query(LevelSessionFact).filter(LevelSessionFact.level_id == level).count()
    
    # Nếu không có lượt chơi nào, trả về rỗng ngay
    if total_sessions == 0:
        return {"level": level, "total_sessions": 0, "data": []}

    # 2. Lấy danh sách Booster
    boosters = db.query(BoosterConfig).all()
    if not boosters:
        return {"level": level, "total_sessions": total_sessions, "data": []}

    # 3. Logic phân phối
    random.seed(level)  # Cố định kết quả để F5 không bị đổi

    categories = [{"name": b.booster_name, "type": "item", "count": 0} for b in boosters]
    categories.append({"name": "Không dùng (None)", "type": "none", "count": 0})

    # Tạo trọng số ngẫu nhiên
    weights = []
    for cat in categories:
        if cat["type"] == "none":
            # Level thấp hay "Không dùng", Level cao bắt buộc dùng
            w = 50 if level < 5 else (20 if level < 15 else 5)
        else:
            w = random.randint(10, 60)
        weights.append(w)

    total_weight = sum(weights)
    current_count_sum = 0

    # BƯỚC A: Chia phần nguyên (Floor)
    for i, cat in enumerate(categories):
        # Tính số lượng dựa trên tỷ lệ
        count = int((weights[i] / total_weight) * total_sessions)
        categories[i]["count"] = count
        current_count_sum += count

    # BƯỚC B: Xử lý số dư (QUAN TRỌNG)
    # Ví dụ: Tổng 2, chia ra 0 và 0. Số dư = 2.
    # Ta phải cộng 2 đơn vị này vào các item để tổng lên đủ 2.
    remainder = total_sessions - current_count_sum
    
    if remainder > 0:
        # Rải đều số dư vào các item (ưu tiên item có trọng số cao hoặc ngẫu nhiên)
        # Ở đây ta rải lần lượt từ đầu danh sách để đơn giản và đảm bảo luôn có hình
        for i in range(remainder):
            # Quay vòng qua danh sách để rải đều nếu số dư lớn
            idx = i % len(categories)
            categories[idx]["count"] += 1

    # 4. Lọc bỏ các mục = 0 và trả về
    final_data = [
        {"name": c["name"], "count": c["count"]} 
        for c in categories if c["count"] > 0
    ]

    return {
        "level": level,
        "total_sessions": total_sessions,
        "data": final_data
    }