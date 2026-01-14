from fastapi import HTTPException

from config import Session
from models import User
from schemas import LoginUserSchema, RegisterUserSchema

from .auth_util import create_access_token, hash_password, verify_password


def login_user(user: LoginUserSchema, db: Session) -> dict:
    """authenticates the user with an jwt token after the appropriate validation and checking"""

    if (user.email == "") or (user.password == ""):
        raise HTTPException(status_code=400, detail="Both feilds must be filled!")

    existing_user: User = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(401, "invalid credentials!")

    is_password_correct = verify_password(user.password, existing_user.password)

    if not is_password_correct:
        raise HTTPException(401, "invalid credentials!")

    token_data = {
        "id": str(existing_user.id),
    }

    new_user = {
        "username": existing_user.username,
        "email": existing_user.email,
    }

    token = create_access_token(data=token_data)

    return {"token": {"access_token": token, "token_type": "bearer"}, "user": new_user}


def register_user(user: RegisterUserSchema, db: Session):
    """registers / saves the user in the db after the appropriate validation and checking"""

    if (user.email == "") or (user.password == "") or (user.username == ""):
        raise HTTPException(status_code=400, detail="Both feilds must be filled!")

    existing_user: User = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists!")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return
