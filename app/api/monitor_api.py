from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.job_log import JobLog
from etl_pipeline import run_etl_job

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 1: Lấy trạng thái mới nhất
@router.get("/status")
def get_latest_status(db: Session = Depends(get_db)):
    # Lấy log mới nhất theo ID giảm dần
    latest_log = db.query(JobLog).order_by(JobLog.id.desc()).first()
    if not latest_log:
        return {"status": "UNKNOWN", "message": "Chưa có dữ liệu chạy", "time": None}
    
    return {
        "status": latest_log.status,
        "message": latest_log.message,
        "time": latest_log.start_time.strftime("%H:%M:%S %d/%m/%Y")
    }

# API 2: Kích hoạt chạy thủ công (Nút bấm)
@router.post("/trigger")
def trigger_etl_job(background_tasks: BackgroundTasks):
    # Chạy ngầm (Background) để không làm đơ giao diện
    background_tasks.add_task(run_etl_job)
    return {"message": "Đã gửi lệnh chạy! Vui lòng đợi..."}