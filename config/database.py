from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autoflush=False, auto=False, bind=engine)
Base = declarative_base()
