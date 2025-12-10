import sys
import os
import traceback
from datetime import datetime, timedelta

# Setup môi trường
sys.path.append(os.getcwd())

from appmetrica_extractor import download_data_persistent, DATA_CONFIG
from load_installations import load_csv_to_db
from app.db.session import SessionLocal
from app.models.job_log import JobLog # Import model mới

def run_etl_job():
    # 1. MỞ NHẬT KÝ & GHI: "ĐANG CHẠY"
    db = SessionLocal()
    current_log = JobLog(status="RUNNING", message="Đang khởi động...")
    db.add(current_log)
    db.commit()
    db.refresh(current_log)
    
    print(f"\n🚀 [ETL] BẮT ĐẦU JOB ID: {current_log.id}")

    try:
        # CẤU HÌNH NGÀY (Logic cũ)
        DATE_FROM = "2025-11-01" 
        DATE_TO = "2025-12-08"

        # PHASE 1: DOWNLOAD
        current_log.message = "Phase 1: Đang tải dữ liệu từ AppMetrica..."
        db.commit()
        
        download_success = True
        for source_type, fields_list in DATA_CONFIG.items():
            if not download_data_persistent(source_type, fields_list, DATE_FROM, DATE_TO):
                download_success = False
                raise Exception(f"Lỗi tải file {source_type}")

        # PHASE 2: LOAD DB
        current_log.message = "Phase 2: Đang nạp vào Database..."
        db.commit()
        
        # Gọi hàm load cũ
        load_csv_to_db()

        # GHI NHẬT KÝ: THÀNH CÔNG
        current_log.status = "SUCCESS"
        current_log.end_time = datetime.now()
        current_log.message = f"Hoàn tất! Dữ liệu từ {DATE_FROM} đến {DATE_TO}"
        db.commit()
        print("✅ ETL JOB XONG!")

    except Exception as e:
        # GHI NHẬT KÝ: THẤT BẠI
        error_msg = str(e)
        print(f"❌ ETL JOB LỖI: {error_msg}")
        traceback.print_exc()
        
        current_log.status = "FAILED"
        current_log.end_time = datetime.now()
        current_log.message = error_msg
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    run_etl_job()