from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserSchema
router = APIRouter()


@router.post("/signup")
def signup(user: UserSchema, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    # Convert Pydantic schema to SQLAlchemy model
    existing_user = user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = User(email=user.email, password=user.password)
    user_repo.add_user(db_user)
    return {"message": "User signed up successfully"}

@router.post("/login")
def login():
    return {"message": "User logged in successfully"}
