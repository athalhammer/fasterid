from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    erdi8_stride: int = 453459956896834
    erdi8_start: str = "b222222222"
    erdi8_safe: bool = False
    fasterid_max_num: int = 50
    fasterid_max_prefix_len: int = 100
    fasterid_filename: str = "last-id.sqlite"
    sqlalchemy_database_url: str | None = None


@lru_cache()
def get_settings():
    return Settings()
