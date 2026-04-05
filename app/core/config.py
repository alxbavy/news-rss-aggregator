from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "news-rss-aggregator"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/news_rss_aggregator"
    telegram_bot_token: SecretStr
    poll_interval_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
