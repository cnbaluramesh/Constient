from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ReceiptsToLedger.core.db import get_db
from ReceiptsToLedger.api.deps import require_role
from ReceiptsToLedger.models.user import User, Role
from ReceiptsToLedger.core.security import hash_password

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str
    role: Role

@router.get("/")
def list_users(db: Session = Depends(get_db), admin=Depends(require_role(Role.admin))):
    return db.query(User).all()

@router.post("/")
def create_user(user_in: UserCreate, db: Session = Depends(get_db), admin=Depends(require_role(Role.admin))):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(400, "User already exists")
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
        organisation_id=admin.organisation_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_role(Role.admin))):
    user = db.query(User).filter(User.id == user_id, User.organisation_id == admin.organisation_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}
