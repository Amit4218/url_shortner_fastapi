from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from utils import DATABASE_URL

engine = create_engine(DATABASE_URL)
session = sessionmaker(autoflush=False, bind=engine)


def get_db():
    """yeilds an instance of the db and closes it afterwards."""
    db = Session()
    try:
        yield db
    finally:
        db.close()
