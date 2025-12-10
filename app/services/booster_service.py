from sqlalchemy.orm import Session
from app.models.booster import Booster
from app.schemas.booster import BoosterCreate, BoosterUpdate

def create_booster(db: Session, booster_in: BoosterCreate):
    db_booster = Booster(
        game_id=booster_in.game_id,
        booster_id_in_log=booster_in.booster_id_in_log,
        friendly_name=booster_in.friendly_name,
        price_usd=booster_in.price_usd
    )
    db.add(db_booster)
    db.commit()
    db.refresh(db_booster)
    return db_booster

def get_boosters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booster).offset(skip).limit(limit).all()

def get_booster_by_id(db: Session, booster_id: int):
    return db.query(Booster).filter(Booster.id == booster_id).first()

def update_booster(db: Session, booster_id: int, booster_in: BoosterUpdate):
    db_booster = get_booster_by_id(db, booster_id)
    if not db_booster:
        return None
    
    update_data = booster_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_booster, key, value)

    db.add(db_booster)
    db.commit()
    db.refresh(db_booster)
    return db_booster

def delete_booster(db: Session, booster_id: int):
    db_booster = get_booster_by_id(db, booster_id)
    if not db_booster:
        return None
    
    db.delete(db_booster)
    db.commit()
    return db_booster