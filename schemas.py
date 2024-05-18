from pydantic import BaseModel
from datetime import datetime

class RentBase(BaseModel):
    book_id: int
    start_date: datetime
    end_date: datetime

class RentCreate(RentBase):
    pass

class Rent(RentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True