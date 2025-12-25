from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "moshpit"
    DEBUG: bool = True 

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    ALLOWED_ORIGINS: List[str] = ["*"]
    MAX_UPLOAD_SIZE_MB: int = 512

    class Config:
        env_file = ".env"


settings = Settings()
