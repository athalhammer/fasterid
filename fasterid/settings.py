from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    erdi8_stride: int
    erdi8_start: str
    erdi8_safe: bool
    fasterid_max_num: int
    fasterid_max_prefix_len: int
    fasterid_filename: str
    sqlalchemy_database_url: str

@lru_cache()
def get_settings():
    return Settings()

