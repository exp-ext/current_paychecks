import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_host: str = os.getenv("POSTGRES_HOST")
    database_port: int = os.getenv("POSTGRES_PORT")
    database_name: str = os.getenv("POSTGRES_DB")
    database_user: str = os.getenv("POSTGRES_USER")
    database_password: str = os.getenv("POSTGRES_PASSWORD")
    secret_key: str = os.getenv("SECRET_KEY")
    access_token_expire: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def database_url(self) -> str:
        return (
            f'postgresql://{quote_plus(self.database_user)}'
            f':{quote_plus(self.database_password)}'
            f'@{self.database_host}:{self.database_port}/{self.database_name}')

    class Config:
        env_file = ".env"


settings = Settings()
