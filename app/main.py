import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse # <--- Import mới
from app.api import admin

from app.api import monitor_api
from app.api import analytics 
from app.models import job_log, booster, analytics as analytics_model, config, job_log
from app.db.base import Base
from app.db.session import engine

# 1. Tạo bảng
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AppMetrica Game Analytics")

# 2. Cấu hình Static (Giữ lại để load file JS/CSS nếu cần)
current_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(current_dir, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# 3. Đăng ký API
app.include_router(monitor_api.router, prefix="/api/monitor", tags=["Monitor"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# 4. ROUTE ĐẶC BIỆT CHO DASHBOARD (LỐI ĐI RIÊNG)
# Truy cập vào /dashboard sẽ đọc thẳng file HTML trả về, không lo lỗi Not Found
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_view():
    # Đường dẫn file dashboard.html
    file_path = os.path.join(static_path, "dashboard.html")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"<h1>Lỗi to đùng: Không tìm thấy file tại {file_path}</h1><p>Bạn hãy kiểm tra xem file dashboard.html đã nằm trong thư mục app/static chưa?</p>"

@app.get("/")
def read_root():
    return {
        "message": "Welcome!",
        "dashboard_link": "http://127.0.0.1:8000/dashboard" # Bấm vào đây cho nhanh
    }

@app.get("/admin", response_class=HTMLResponse)
def admin_view():
    try:
        with open("app/static/admin.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Lỗi: Chưa tạo file app/static/admin.html</h1>"