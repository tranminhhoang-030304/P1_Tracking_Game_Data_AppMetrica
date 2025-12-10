from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.booster import BoosterCreate, BoosterResponse, BoosterUpdate
from app.services import booster_service

router = APIRouter()

@router.post("/", response_model=BoosterResponse)
def create_booster(booster_in: BoosterCreate, db: Session = Depends(get_db)):
    return booster_service.create_booster(db=db, booster_in=booster_in)

@router.get("/", response_model=List[BoosterResponse])
def read_boosters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return booster_service.get_boosters(db, skip=skip, limit=limit)

@router.put("/{booster_id}", response_model=BoosterResponse)
def update_booster(booster_id: int, booster_in: BoosterUpdate, db: Session = Depends(get_db)):
    booster = booster_service.update_booster(db, booster_id, booster_in)
    if not booster:
        raise HTTPException(status_code=404, detail="Không tìm thấy Booster ID này")
    return booster

@router.delete("/{booster_id}")
def delete_booster(booster_id: int, db: Session = Depends(get_db)):
    booster = booster_service.delete_booster(db, booster_id)
    if not booster:
        raise HTTPException(status_code=404, detail="Không tìm thấy Booster ID này")
    return {"message": "Đã xóa Booster thành công!"}