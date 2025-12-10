from pydantic import BaseModel
from typing import Optional

class BoosterBase(BaseModel):
    booster_id_in_log: str  # ID trong log (VD: pack_starter)
    friendly_name: str      # Tên hiển thị (VD: Gói Tân Thủ)
    price_usd: float        # Giá tiền
    game_id: int            # Gói này thuộc Game nào

class BoosterCreate(BoosterBase):
    pass

class BoosterUpdate(BaseModel):
    booster_id_in_log: Optional[str] = None
    friendly_name: Optional[str] = None
    price_usd: Optional[float] = None
    game_id: Optional[int] = None

class BoosterResponse(BoosterBase):
    id: int

    class Config:
        from_attributes = True