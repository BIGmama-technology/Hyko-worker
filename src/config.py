
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings from the containers env vars."""

    HOST: str
    REDIS_USERNAME: str
    REDIS_PASS: str
    USER_ID: str
    WORKER_ID: str

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
