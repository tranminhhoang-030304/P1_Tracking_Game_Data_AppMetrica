from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Tạo động cơ kết nối (Engine)
engine = create_engine(settings.DATABASE_URL)

# Tạo phiên làm việc (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Hàm dependency để lấy DB session (dùng cho API sau này)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()