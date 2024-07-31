from pydantic_settings import BaseSettings
import os


class AuthConfig(BaseSettings):
    
    #################################### auth related ####################################
    JWT_ACCESS_SECRET_KEY: str = "9d9bc4d77ac3a6fce1869ec8222729d2"
    JWT_REFRESH_SECRET_KEY: str = "fdc5635260b464a0b8e12835800c9016"
    ENCRYPTION_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    NEW_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # Google Auth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_USERINFO_URL: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    GOOGLE_AUTH_URL: str = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"
    # openapi
    # OPENAPI_PROJECT_SECRET_KEY: str
    #################################### auth related ####################################
    
    #################################### admin ####################################
    ADMIN_SECRET_KEY: str = "Hv9LGqARc473ceBUYDw1FR0QaXOA3Ky4"
    #################################### admin ####################################
    
    
auth_settings = AuthConfig()