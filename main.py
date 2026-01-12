from fastapi import FastAPI

from config import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict:
    return {"status": "200", "message": "Api is healthy"}
