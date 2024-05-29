from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings from the containers env vars."""

    HOST: str
    REDIS_USERNAME: str
    REDIS_PASS: str
    USER_ID: str
    WORKER_ID: str

    @computed_field
    @property
    def URL(self) -> str:  # noqa: N802
        """Construct endpoint url."""
        return f"https://api.{self.HOST}/workers/{self.USER_ID}/{self.WORKER_ID}/system-info"

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()  # type: ignore
