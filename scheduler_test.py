from apscheduler.schedulers.blocking import BlockingScheduler
from etl_pipeline import run_etl_job
from datetime import datetime
import sys

# Khởi tạo
scheduler = BlockingScheduler()

def job_wrapper():
    print(f"\n⚡ [TEST MODE] Kích hoạt Job lúc: {datetime.now().strftime('%H:%M:%S')}")
    try:
        run_etl_job()
        print("✅ Job hoàn tất.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

# Cấu hình: Chạy lặp lại mỗi 30 giây (seconds=30)
scheduler.add_job(job_wrapper, 'interval', seconds=30)

if __name__ == "__main__":
    print(f"{'='*50}")
    print("🧪 ĐANG CHẠY CHẾ ĐỘ TEST (Chạy mỗi 30 giây)")
    print("👉 Hãy đợi 30s để thấy Job tự động chạy lần đầu tiên...")
    print("❌ Nhấn Ctrl+C để dừng và chuyển sang bản chính thức")
    print(f"{'='*50}\n")
    
    # Mẹo: Gọi hàm 1 lần ngay lập tức để bạn đỡ phải chờ 30s mới thấy kết quả
    print("🚀 [TEST] Chạy thử lần đầu ngay bây giờ:")
    job_wrapper() 
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Đã dừng test.")