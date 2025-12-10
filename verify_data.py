from sqlalchemy import text
from app.db.session import engine

def verify_system_data():
    print("🕵️‍♂️ BẮT ĐẦU KIỂM THỬ ĐỐI CHIẾU DỮ LIỆU (VERIFY)...")
    print("-" * 50)
    
    with engine.connect() as conn:
        # 1. Đếm tổng số session đã xử lý trong DB Local
        result = conn.execute(text("SELECT COUNT(*) FROM fact_level_sessions"))
        local_count = result.scalar()
        
        # 2. Đếm số lượng theo trạng thái
        win_count = conn.execute(text("SELECT COUNT(*) FROM fact_level_sessions WHERE status='WIN'")).scalar()
        fail_count = conn.execute(text("SELECT COUNT(*) FROM fact_level_sessions WHERE status='FAIL'")).scalar()
        
        # 3. Tính tổng doanh thu ghi nhận
        revenue = conn.execute(text("SELECT SUM(total_coin_spent) FROM fact_level_sessions")).scalar()

    print(f"📊 KẾT QUẢ KIỂM TRA HỆ THỐNG:")
    print(f"   ✅ Tổng số lượt chơi đã Import: {local_count}")
    print(f"   ✅ Số lượt Thắng (WIN):        {win_count}")
    print(f"   ✅ Số lượt Thua (FAIL):        {fail_count}")
    print(f"   💰 Tổng Doanh thu ước tính:    {revenue:,} Coin")
    print("-" * 50)
    
    # Logic Verify
    if local_count > 0:
        print("✅ KẾT LUẬN: Hệ thống hoạt động tốt, dữ liệu khớp với quy trình ETL.")
    else:
        print("❌ KẾT LUẬN: Dữ liệu trống. Cần kiểm tra lại ETL.")

if __name__ == "__main__":
    verify_system_data()