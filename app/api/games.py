from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.game import GameCreate, GameResponse, GameUpdate
from app.services import game_service

router = APIRouter()

# API 1: Tạo game mới
@router.post("/", response_model=GameResponse)
def create_game(game_in: GameCreate, db: Session = Depends(get_db)):
    return game_service.create_new_game(db=db, game_in=game_in)

# API 2: Lấy danh sách game
@router.get("/", response_model=List[GameResponse])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = game_service.get_all_games(db, skip=skip, limit=limit)
    return games

# API 3: Cập nhật thông tin Game
@router.put("/{game_id}", response_model=GameResponse)
def update_game(game_id: int, game_in: GameUpdate, db: Session = Depends(get_db)):
    game = game_service.update_game(db, game_id, game_in)
    if not game:
        raise HTTPException(status_code=404, detail="Không tìm thấy Game ID này")
    return game

# API 4: Xóa Game
@router.delete("/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = game_service.delete_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Không tìm thấy Game ID này")
    return {"message": "Đã xóa game thành công!"}