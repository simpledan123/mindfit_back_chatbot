from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db, get_current_user
from core.security import verify_password
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate, UserPasswordUpdate
import crud.user

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    return crud.user.create_user(db, user_create)

@router.patch("/me", response_model=UserRead)
def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.user.update_user(db, current_user, user_update)

@router.delete("/me")
def delete_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.user.delete_user(db, current_user)
    return {"detail": "User deleted"}

@router.patch("/me/password")
def change_password(password_update: UserPasswordUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")