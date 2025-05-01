import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    # Secret key for securely signing the session cookie and other secrets
    SECRET_KEY = os.getenv("SECRETE_KEY")  # Should be a long, random string

    # Database connection URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # Example: "sqlite:///site.db" or a PostgreSQL URL

    # Enables or disables SQLAlchemy's event system (track modifications)
    SQLALCHEMY_TRACK_MODIFICATION = os.getenv("SQLALCHEMY_TRACK_MODIFICATION")  # Should typically be "False"

    # Secret key for JWT authentication
    JWT_SECRET_KEY = os.getenv("JWT_SECRETE_KEY")  # Should be a long, random string for signing JWT tokens

    # Enables or disables JWT token blacklisting
    JWT_BLACKLIST_ENABLED = os.getenv("JWT_BLACKLIST_ENABLED")  # Should be "True" or "False"

    # Determines which types of tokens (access, refresh) to check against the blacklist
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv("JWT_BLACKLIST_TOKEN_CHECKS")  # Example: "access, refresh"

    # Expiration time for access tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=8)  # Adjust as needed for security and usability

    # Expiration time for refresh tokens
    JWT_REFRESH_TOKEN = timedelta(days=7)  # Adjust as needed for security and usability

    # Domain URL for the application
    DOMAIN_URL = "http://127.0.0.1:5000"  # Update this if deploying to a live server