from pydantic import BaseSettings, EmailStr
from dotenv import load_dotenv

import os

load_dotenv()

class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL: str = os.environ.get('SQLALCHEMY_DATABASE_URL')
    DB_ECHO: bool = False
    HEALTH_CHECK_URL: str = os.environ.get('HEALTH_CHECK_URL')

    REDIS_NAME: str = os.environ.get('REDIS_NAME')
    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: str = os.environ.get('REDIS_PORT')
    REDIS_DB: str = os.environ.get('REDIS_DB')
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD')

    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM: str = os.environ.get('ALGORITHM')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()