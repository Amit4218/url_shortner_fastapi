import os

from dotenv import load_dotenv

ENV = os.getenv("ENV", "DEV")


ENV_PATH = ".env.local" if ENV == "DEV" else ".env"

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

SECURITY_KEY = os.getenv("SECURITY_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRY = os.getenv("ACCESS_TOKEN_EXPIRY")

FRONTEND_URL = os.getenv("FRONTEND_URL")
