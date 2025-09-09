from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ReceiptsToLedger.core.security import create_access_token, verify_password
from ReceiptsToLedger.core.db import get_db
from ReceiptsToLedger.models.user import User
from sqlalchemy.orm import Session
from datetime import timedelta
from ReceiptsToLedger.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"   # 👈 Swagger needs this
    }
