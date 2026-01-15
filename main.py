from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import engine, get_db
from core import (
    get_current_user,
    get_redirect_url,
    get_url_metadata,
    login_user,
    register_user,
    save_url,
)
from models import User
from schemas import (
    LoginResponseSchema,
    LoginUserSchema,
    RegisterUserSchema,
    ResponseSchema,
    UrlSchema,
)
from utils import ENV, FRONTEND_URL, Base, generate_unique_url

is_production = False if ENV == "DEV" else True


app = FastAPI(title="url_shortner backend", openapi_url=None, redoc_url=None)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=[FRONTEND_URL],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


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
async def short_url(
    data: UrlSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    unique_url = generate_unique_url(db=db)

    url = save_url(
        db=db,
        original_url=data.original_url,
        id=str(current_user.id),
        unique_url=unique_url,
    )

    return ResponseSchema(
        status=201,
        message="short url Created successfully",
        data=url,
    )


@app.get("/r/{short_url}", response_model=ResponseSchema)
async def get_original_url(
    short_url: str, request: Request, db: Session = Depends(get_db)
) -> ResponseSchema:
    original_url = get_redirect_url(db=db, url=short_url, request_obj=request)

    return ResponseSchema(
        status=200, message="success", data={"original_url": original_url}
    )


@app.get("/get_metadata", response_model=ResponseSchema)
async def get_metadata(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    data = get_url_metadata(db=db, user_id=str(current_user.id))

    return ResponseSchema(status=200, message="data fetched successfully", data=data)
