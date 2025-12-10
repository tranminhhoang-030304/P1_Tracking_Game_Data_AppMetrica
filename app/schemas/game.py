from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 1. Khuôn mẫu cơ bản (Dùng chung cho lúc tạo và lúc xem)
class GameBase(BaseModel):
    name: str
    bundle_id: str
    platform: str
    appmetrica_app_id: str
    appmetrica_api_key: str
    is_active: bool = True

# 2. Khuôn mẫu dùng lúc TẠO mới (Input)
class GameCreate(GameBase):
    pass 

# Class này dùng cho việc UPDATE (Các trường đều không bắt buộc)
class GameUpdate(BaseModel):
    name: Optional[str] = None
    bundle_id: Optional[str] = None
    platform: Optional[str] = None
    appmetrica_app_id: Optional[str] = None
    appmetrica_api_key: Optional[str] = None
    is_active: Optional[bool] = None

# 3. Khuôn mẫu dùng lúc TRẢ VỀ dữ liệu (Output)
class GameResponse(GameBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Giúp chuyển đổi từ SQLAlchemy Model sang Pydantic