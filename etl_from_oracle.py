import oracledb
import pandas as pd
import json
import random
import traceback
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.analytics import LevelSessionFact
from app.models.config import SystemConfig
from app.models.job_log import JobLog

# Hàm hỗ trợ lấy config nhanh từ DB
def get_config_value(session, key, default=None):
    cfg = session.query(SystemConfig).filter_by(key=key).first()
    return cfg.value if cfg else default

EVENT_MAPPING = { "Win_Battle": "WIN", "Lose_Battle": "FAIL" }

def sync_from_oracle_fixed():
    session = Session(engine)
    
    # 1. TẠO LOG: BẮT ĐẦU CHẠY
    print("\n🚀 [ETL] Bắt đầu tiến trình đồng bộ...")
    job = JobLog(
        job_name="ETL Oracle Sync",
        status="RUNNING",
        message="Đang kết nối Oracle...",
        start_time=datetime.utcnow()
    )
    session.add(job)
    session.commit() # Commit để lấy job.id
    
    conn = None
    try:
        # 2. ĐỌC CẤU HÌNH TỪ DB (Thay vì Hardcode)
        oracle_user = get_config_value(session, "ORACLE_USER")
        oracle_pass = get_config_value(session, "ORACLE_PASS")
        oracle_host = get_config_value(session, "ORACLE_HOST")
        oracle_port = get_config_value(session, "ORACLE_PORT")
        oracle_sid = get_config_value(session, "ORACLE_SERVICE")
        
        # Kiểm tra nếu thiếu config
        if not all([oracle_user, oracle_pass, oracle_host]):
            raise Exception("Thiếu cấu hình Oracle trong bảng system_configs!")

        dsn = f"{oracle_host}:{oracle_port}/{oracle_sid}"
        
        # 3. KẾT NỐI ORACLE
        conn = oracledb.connect(user=oracle_user, password=oracle_pass, dsn=dsn)
        print("✅ Kết nối Oracle thành công (Từ cấu hình DB).")
        
        # 4. LẤY DỮ LIỆU
        sql = """
            SELECT SESSION_ID, APPMETRICA_DEVICE_ID, EVENT_NAME, EVENT_JSON 
            FROM SKW_ID.APPMETRICA_EVENTS_RAW 
            WHERE EVENT_NAME IN ('Win_Battle', 'Lose_Battle')
            FETCH FIRST 8000 ROWS ONLY
        """
        df_oracle = pd.read_sql(sql, conn)
        
        row_count = len(df_oracle)
        print(f"📥 Tải được {row_count} dòng. Đang xử lý...")
        
        # Cập nhật log: Đang xử lý
        job.message = f"Đã tải {row_count} dòng. Đang xử lý..."
        session.commit()

        # 5. XỬ LÝ DỮ LIỆU (TRANSFORM)
        new_records = []
        count_success = 0
        
        for index, row in df_oracle.iterrows():
            try:
                # Bóc tách JSON (Logic cũ vẫn giữ nguyên)
                raw_lob = row.get('EVENT_JSON')
                if hasattr(raw_lob, 'read'): json_str = raw_lob.read()
                else: json_str = str(raw_lob)
                
                if not json_str: continue
                outer_json = json.loads(json_str)
                
                inner_str = outer_json.get('event_json')
                params = json.loads(inner_str) if (inner_str and isinstance(inner_str, str)) else outer_json
                
                raw_level = params.get('battleID')
                if not raw_level: continue
                level_id = int(raw_level)
                
                event_name = row.get('EVENT_NAME')
                status = EVENT_MAPPING.get(event_name, "UNKNOWN")
                
                simulated_coin = level_id * 10 + random.randint(0, 50)
                if status == "FAIL": simulated_coin += 50
                
                record = LevelSessionFact(
                    session_id=str(row.get('SESSION_ID')),
                    user_id=str(row.get('APPMETRICA_DEVICE_ID')),
                    game_id="4769050",
                    level_id=level_id,
                    status=status,
                    total_coin_spent=simulated_coin,
                    total_boosters_used=1,
                    play_time_seconds=random.randint(30, 180),
                    event_timestamp=datetime.utcnow()
                )
                new_records.append(record)
                count_success += 1
            except:
                continue

        # 6. LƯU VÀO DB
        for rec in new_records:
            session.merge(rec)
        
        # 7. CHỐT LOG: THÀNH CÔNG
        job.status = "SUCCESS"
        job.rows_imported = count_success
        job.message = "Hoàn tất thành công."
        job.end_time = datetime.utcnow()
        
        session.commit()
        print(f"✅ [ETL] Hoàn tất! Đã import {count_success} dòng.")

    except Exception as e:
        # 8. CHỐT LOG: THẤT BẠI
        print(f"❌ [ETL] Lỗi: {e}")
        job.status = "FAILED"
        job.message = str(e)[:500] # Cắt ngắn lỗi nếu dài quá
        job.end_time = datetime.utcnow()
        session.commit()
        
    finally:
        if conn: conn.close()
        session.close()

if __name__ == "__main__":
    sync_from_oracle_fixed()