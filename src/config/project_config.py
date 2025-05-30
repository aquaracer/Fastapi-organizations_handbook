import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = os.getenv('POSTGRES_HOST')
    DB_PORT: int = os.getenv('POSTGRES_PORT')
    DB_USER: str = os.getenv('POSTGRES_USER')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    DB_DRIVER: str = os.getenv('POSTGRES_DRIVER')
    DB_NAME: str = os.getenv('POSTGRES_DB')

    API_KEY: str = os.getenv("API_KEY")

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
