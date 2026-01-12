from fastapi import FastAPI

from config import engine
from schemas import ResponseSchema
from utils import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict:
    return {"status": 200, "message": "Server is running..."}


@app.post("/login")
async def login():
    pass


@app.post("/register")
async def register(user):
    pass


@app.post("/short_url")
async def short_url(data):
    pass


@app.get("/{short_url}")
async def get_original_url(short_url) -> ResponseSchema:
    return ResponseSchema(status=200, message="success")
