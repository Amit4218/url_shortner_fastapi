import random
from string import ascii_letters, digits

from sqlalchemy.orm import Session

from models import NotRegisteredUrls, Urls


def generate_unique_url(length: int = 6, db: Session | None = None) -> str:
    """Generates a unique list of 6 characters by default, for unique url"""
    if db is None:
        raise ValueError("Database session cannot be None")

    while True:
        unique_url: str = "".join(random.choices(ascii_letters + digits, k=length))

        registered_url = db.query(Urls).filter(Urls.short_url == unique_url).first()

        temp_urls = (
            db.query(NotRegisteredUrls)
            .filter(NotRegisteredUrls.short_url == unique_url)
            .first()
        )

        if not registered_url and not temp_urls:
            return unique_url
