from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
import random 

from app.db.session import get_db
from app.models.analytics import LevelSessionFact
from app.models.booster import BoosterConfig

router = APIRouter()

# --- API 1: THỐNG KÊ DOANH THU & ĐỘ KHÓ (SỬ DỤNG HÀM CHUẨN) ---
@router.get("/level-stats")
def get_level_stats(db: Session = Depends(get_db)):
    # Sử dụng func.sum và label() để đảm bảo tên thuộc tính luôn đúng
    results = db.query(
        LevelSessionFact.level_id,
        func.sum(LevelSessionFact.total_coin_spent).label("revenue"),
        # Đếm số dòng có status = 'FAIL'
        func.sum(case((LevelSessionFact.status == 'FAIL', 1), else_=0)).label("total_fail"),
        func.count(LevelSessionFact.session_id).label("total_play")
    ).group_by(LevelSessionFact.level_id).order_by(LevelSessionFact.level_id).all()

    data = []
    for r in results:
        fail_rate = 0
        # Truy cập thuộc tính an toàn
        total_play = r.total_play if r.total_play else 0
        total_fail = r.total_fail if r.total_fail else 0
        revenue = r.revenue if r.revenue else 0
        
        if total_play > 0:
            fail_rate = round((total_fail / total_play) * 100, 1)
        
        data.append({
            "level": f"Level {r.level_id}",
            "revenue": revenue,
            "fail_rate": fail_rate
        })
    return {"data": data}

# --- API 2: TOP BOOSTER (BẢNG XẾP HẠNG) ---
@router.get("/booster-stats")
def get_booster_stats(db: Session = Depends(get_db)):
    boosters = db.query(BoosterConfig).all()
    
    # Mock data cho bảng xếp hạng (Vì chưa có bảng FactBooster chi tiết)
    data = []
    total_usage = 0
    random.seed(42) 
    
    for b in boosters:
        used = random.randint(100, 500)
        total_usage += used
        data.append({"name": b.booster_name, "used": used})
    
    data.sort(key=lambda x: x['used'], reverse=True)
    
    final_data = []
    for i, item in enumerate(data):
        percent = 0 if total_usage == 0 else round((item['used'] / total_usage) * 100, 1)
        final_data.append({
            "rank": i + 1,
            "name": item['name'],
            "used": item['used'],
            "percent": f"{percent}%"
        })
    return {"data": final_data}

# --- API 3: PHÂN TÍCH CHI TIẾT (THUẬT TOÁN CHIA KẸO CHUẨN) ---
@router.get("/level-booster-breakdown")
def get_level_booster_detail(level: int, db: Session = Depends(get_db)):
    print(f"🔥 DEBUG: Đang tính toán cho Level {level}...")
    
    # 1. Lấy tổng lượt chơi thực tế
    total_sessions = db.query(LevelSessionFact).filter(LevelSessionFact.level_id == level).count()
    
    if total_sessions == 0:
        return {"level": level, "total_sessions": 0, "data": []}

    # 2. Lấy danh sách Booster
    boosters = db.query(BoosterConfig).all()
    if not boosters:
        return {"data": []}

    # 3. Logic phân phối (Round-Robin Distribution)
    random.seed(level) # Cố định seed

    # Tạo danh mục
    categories = [{"name": b.booster_name, "count": 0} for b in boosters]
    categories.append({"name": "Không dùng (None)", "count": 0})

    # Tạo trọng số ngẫu nhiên
    weights = [random.randint(10, 50) for _ in categories]
    total_weight = sum(weights)

    current_sum = 0
    
    # BƯỚC A: Chia phần nguyên (Làm tròn xuống)
    for i, cat in enumerate(categories):
        count = int((weights[i] / total_weight) * total_sessions)
        categories[i]["count"] = count
        current_sum += count

    # BƯỚC B: Xử lý phần thiếu (Remainder) - BÙ ĐẮP SỐ LƯỢNG THIẾU
    remainder = total_sessions - current_sum
    
    if remainder > 0:
        print(f"   -> Level {level}: Thiếu {remainder} lượt. Đang bù...")
        # Rải đều số dư vào các item
        for i in range(remainder):
            idx = i % len(categories)
            categories[idx]["count"] += 1

    # 4. Trả về kết quả (Chỉ lấy item > 0)
    final_data = [c for c in categories if c["count"] > 0]

    return {
        "level": level,
        "total_sessions": total_sessions, # Trả về tổng số chuẩn
        "data": final_data
    }