from sqlalchemy.orm import Session
from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate

# Hàm tạo game mới
def create_new_game(db: Session, game_in: GameCreate):
    # Chuyển dữ liệu từ Schema sang Model
    db_game = Game(
        name=game_in.name,
        bundle_id=game_in.bundle_id,
        platform=game_in.platform,
        appmetrica_app_id=game_in.appmetrica_app_id,
        appmetrica_api_key=game_in.appmetrica_api_key,
        is_active=game_in.is_active
    )
    db.add(db_game)
    db.commit()      # Lưu vào DB
    db.refresh(db_game) # Lấy lại thông tin (bao gồm ID vừa tự sinh)
    return db_game

# Hàm lấy danh sách game
def get_all_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Game).offset(skip).limit(limit).all()

# Hàm lấy 1 game theo ID (để check xem game có tồn tại không)
def get_game_by_id(db: Session, game_id: int):
    return db.query(Game).filter(Game.id == game_id).first()

# Hàm CẬP NHẬT (Update)
def update_game(db: Session, game_id: int, game_in: GameUpdate):
    db_game = get_game_by_id(db, game_id)
    if not db_game:
        return None
    
    # Chỉ cập nhật những trường người dùng gửi lên
    update_data = game_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_game, key, value)

    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

# Hàm XÓA (Delete)
def delete_game(db: Session, game_id: int):
    db_game = get_game_by_id(db, game_id)
    if not db_game:
        return None
    
    db.delete(db_game)
    db.commit()
    return db_game