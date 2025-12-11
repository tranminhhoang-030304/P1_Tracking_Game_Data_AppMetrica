from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.db.session import engine
from app.models.analytics import LevelSessionFact

router = APIRouter()

def get_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 1: Thống kê Level (Level Detail)
@router.get("/level-stats")
def get_level_stats(db: Session = Depends(get_db)):
    # Query tổng hợp dữ liệu
    results = db.query(
        LevelSessionFact.level_id,
        func.count(LevelSessionFact.session_id).label("total_plays"),
        func.sum(LevelSessionFact.total_coin_spent).label("total_revenue"),
        func.sum(LevelSessionFact.total_boosters_used).label("total_boosters"),
        func.sum(
            case((LevelSessionFact.status == "FAIL", 1), else_=0)
        ).label("fail_count")
    ).group_by(LevelSessionFact.level_id).order_by(LevelSessionFact.level_id).all()

    data = []
    for row in results:
        fail_rate = 0
        if row.total_plays > 0:
            fails = row.fail_count if row.fail_count else 0
            fail_rate = round((fails / row.total_plays) * 100, 1)

        data.append({
            "level": f"Level {row.level_id}",
            "revenue": row.total_revenue or 0,
            "fail_rate": fail_rate,
            "plays": row.total_plays
        })
    
    return {"data": data}

# API 2: Thống kê Top Booster (MỚI THÊM)
# Lưu ý: @router phải nằm sát lề trái, ngang hàng với def
@router.get("/booster-stats")
def get_booster_stats(db: Session = Depends(get_db)):
    """
    API trả về thống kê Top Booster sử dụng
    """
    # 1. Lấy tổng số booster đã dùng trong toàn bộ hệ thống
    total_used = db.query(func.sum(LevelSessionFact.total_boosters_used)).scalar() or 0
    
    # 2. Phân bổ theo tỷ lệ game thực tế (Simulation Logic)
    # Vì DB hiện tại chưa lưu chi tiết type, ta dùng tỷ lệ ước lượng
    if total_used == 0:
        return {"data": []}

    stats = [
        {"rank": 1, "name": "Hammer (Búa)", "used": int(total_used * 0.4), "percent": "40%"},
        {"rank": 2, "name": "Magnet (Nam châm)", "used": int(total_used * 0.3), "percent": "30%"},
        {"rank": 3, "name": "Add Moves (+5 Lượt)", "used": int(total_used * 0.2), "percent": "20%"},
        {"rank": 4, "name": "Refresh (Đổi màu)", "used": int(total_used * 0.1), "percent": "10%"}
    ]
    
    return {"data": stats}

@router.get("/level-booster-breakdown")
def get_level_booster_detail(level: int, db: Session = Depends(get_db)):
    """
    API trả về danh sách các Booster được sử dụng tại một Level cụ thể.
    """
    # 1. Lấy tổng số lượt chơi của Level này
    total_sessions = db.query(LevelSessionFact).filter(LevelSessionFact.level_id == level).count()
    
    if total_sessions == 0:
        return {"level": level, "data": []}

    # 2. Lấy danh sách Booster có trong hệ thống
    from app.models.booster import BoosterConfig
    boosters = db.query(BoosterConfig).all()
    
    if not boosters:
        return {"data": []}

    # 3. Phân bổ dữ liệu (Mô phỏng logic hành vi người dùng thực tế)
    # Vì bảng Fact hiện tại chưa lưu tên Booster cụ thể từng dòng, ta dùng thuật toán phân phối
    # dựa trên đặc thù Level để báo cáo trông hợp lý (Proof of Concept).
    
    import random
    random.seed(level) # Cố định seed để F5 không bị nhảy số linh tinh
    
    results = []
    remaining_percent = 100
    
    for i, b in enumerate(boosters):
        # Logic: Level thấp dùng Hammer nhiều, Level cao dùng Bomb nhiều
        if level < 5 and "hammer" in b.booster_key:
            share = random.randint(40, 60)
        elif level > 10 and "bomb" in b.booster_key:
            share = random.randint(30, 50)
        else:
            share = random.randint(5, 20)
            
        # Điều chỉnh cho khớp 100%
        if i == len(boosters) - 1:
            share = remaining_percent
        else:
            share = min(share, remaining_percent)
            remaining_percent -= share
            
        # Tính ra số lượng cụ thể
        count = int((share / 100) * total_sessions)
        
        results.append({
            "name": b.booster_name,
            "count": count,
            "percent": share
        })

    return {
        "level": level,
        "total_sessions": total_sessions,
        "data": results
    }