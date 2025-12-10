from sqlalchemy import text
from app.db.session import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'Kết nối thành công!'"))
            print("✅ " + result.scalar())
    except Exception as e:
        print("❌ Lỗi kết nối:", e)

if __name__ == "__main__":
    test_connection()