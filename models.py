from sqlalchemy import Column, Integer, DateTime
from database import Base

class Rent(Base):
    __tablename__ = "rents"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    class Config:
        from_attributes = True