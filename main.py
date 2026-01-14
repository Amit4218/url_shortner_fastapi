from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import engine, get_db
from core import get_current_user, login_user, register_user
from models import User
from schemas import (
    LoginResponseSchema,
    LoginUserSchema,
    RegisterUserSchema,
    ResponseSchema,
)
from utils import ENV, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)
is_production = False if ENV == "DEV" else True


@app.get("/")
def read_root() -> dict:
    return {"status": 200, "message": "Server is running..."}


@app.post("/login", response_model=LoginResponseSchema)
async def login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    result = login_user(
        LoginUserSchema(email=data.username, password=data.password),
        db=db,
    )

    return LoginResponseSchema(
        status=200,
        message="logged in successfully",
        data=result["user"],
        access_token=result["token"]["access_token"],
        token_type=result["token"]["token_type"],
    )


@app.post("/register", response_model=ResponseSchema)
async def register(data: RegisterUserSchema, db: Session = Depends(get_db)):
    register_user(data, db)
    return ResponseSchema(status=201, message="user registered successful")


@app.post("/short_url", response_model=ResponseSchema)
async def short_url(data: dict, current_user: User = Depends(get_current_user)):
    return ResponseSchema(
        status=200,
        message="authorized",
        data={"user_id": str(current_user.id)},
    )


@app.get("/{short_url}", response_model=ResponseSchema)
async def get_original_url(short_url) -> ResponseSchema:
    return ResponseSchema(status=200, message="success")
