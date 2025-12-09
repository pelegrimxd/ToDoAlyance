from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )
    postgres_user: str = Field(
        min_length=1,
        description="postgres user",
    )
    postgres_password: str = Field(
        min_length=1,
        description="postgres password",
    )
    postgres_db: str = Field(
        min_length=1,
        description="postgres db name",
    )
    postgres_host: str = Field(
        min_length=1,
        description="postgres db host",
    )
    postgres_port: str = Field(
        min_length=1,
        description="postgres db port",
    )


app_config = AppConfig()
