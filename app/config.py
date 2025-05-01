import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRETE_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATION = os.getenv("SQLALCHEMY_TRACK_MODIFICATION")
    JWT_SECRET_KEY = os.getenv("JWT_SECRETE_KEY")
    JWT_BLACKLIST_ENABLED = os.getenv("JWT_BLACKLIST_ENABLED")
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv("JWT_BLACKLIST_TOKEN_CHECKS")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN = timedelta(days=7)
    DOMAIN_URL = "http://127.0.0.1:5000"
