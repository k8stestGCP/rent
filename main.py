from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import Rent, RentCreate
from crud import create_rent, get_rents_by_user, get_rent_by_id
from dependencies import verify_token
import jwt
from database import init_db

app = FastAPI()
init_db()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/rents/", response_model=Rent)
async def create_new_rent(rent: RentCreate, request: Request, db: Session = Depends(get_db)):
    verified = await verify_token(request, rent.book_id)
    token = request.headers.get("Authorization")
    token = token.split("Bearer ")[1]

    decoded = jwt.decode(token, options={"verify_signature": False}) # works in PyJWT >= v2.0
    if verified:
        try:
            print("I GOT HERE BUDDY")

            return create_rent(db=db, rent=rent, user_id=decoded["id"])
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User verification failed"
        )

@app.get("/rents/", response_model=list[Rent])
def read_user_rents(user=Depends(verify_token), db: Session = Depends(get_db)):
    rents = get_rents_by_user(db=db, user_id=user.id)
    return rents

@app.get("/rents/{rent_id}", response_model=Rent)
def read_rent(rent_id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    rent = get_rent_by_id(db=db, rent_id=rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")
    if rent.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this rent")
    return rent