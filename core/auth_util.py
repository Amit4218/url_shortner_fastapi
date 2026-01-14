from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import get_db
from models import User
from utils import ACCESS_TOKEN_EXPIRY, ALGORITHM, SECURITY_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

access_token_expiry = int(f"{ACCESS_TOKEN_EXPIRY}")


def hash_password(password: str) -> str:
    """used to hashes the user password"""
    return password_context.hash(secret=password)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    """verifies the user plain_pass with the hashed password"""
    return password_context.verify(secret=plain_pass, hash=hashed_pass)


def create_access_token(data: dict) -> str:
    "creates an jwt token for the user authorization"
    to_encode = data.copy()
    expire = datetime.now((timezone.utc)) + timedelta(days=access_token_expiry)
    to_encode.update({"exp": expire})
    return jwt.encode(claims=to_encode, key=SECURITY_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"},
    )

    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise credentials_exception

    return user
