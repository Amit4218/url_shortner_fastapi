import random
from string import ascii_letters, digits

from sqlalchemy.orm import Session

from models import Urls


def generate_unique_url(length: int = 6, db: Session | None = None) -> str:
    """Generates a unique list of 7 characters by default, for unique url"""
    if db is None:
        raise ValueError("Database session cannot be None")

    while True:
        unique_url: str = "".join(random.choices(ascii_letters + digits, k=length))

        exits = db.query(Urls).filter(Urls.short_url == unique_url).first()

        if not exits:
            return unique_url
