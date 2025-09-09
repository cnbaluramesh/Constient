from fastapi import Depends, HTTPException, Header,Security
from sqlalchemy.orm import Session
from jose import JWTError

from ReceiptsToLedger.core.db import get_db
from ReceiptsToLedger.core.security import decode_access_token
from ReceiptsToLedger.models.user import User, Role
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=True, scheme_name="BearerAuth")

def get_current_user(
    db: Session = Depends(get_db),
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    token = creds.credentials
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_org(user: User = Depends(get_current_user)):
    if not user.organisation_id:
        raise HTTPException(status_code=400, detail="User not assigned to an organisation")
    return user.organisation_id

def require_role(role: Role):
    def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
