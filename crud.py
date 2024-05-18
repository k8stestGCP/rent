from sqlalchemy.orm import Session
from models import Rent
from schemas import RentCreate

def create_rent(db: Session, rent: RentCreate, user_id: int):
    existing_rent = db.query(Rent).filter(Rent.book_id == rent.book_id, Rent.user_id == user_id).first()
    if existing_rent:
        raise ValueError("Rent already exists for this book and user")
    
    db_rent = Rent(book_id=rent.book_id, start_date=rent.start_date, end_date=rent.end_date, user_id=user_id)
    db.add(db_rent)
    db.commit()
    db.refresh(db_rent)
    return db_rent

def get_rents_by_user(db: Session, user_id: int):
    return db.query(Rent).filter(Rent.user_id == user_id).all()

def get_rent_by_id(db: Session, rent_id: int):
    return db.query(Rent).filter(Rent.id == rent_id).first()