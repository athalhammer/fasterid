from enum import Enum
from pydantic_settings import BaseSettings


class StorageType(Enum):
    FILE_LOG = "file-log"
    FILE = "file-latest"
    DATABASE = "database"


class Settings(BaseSettings):
    erdi8_stride: int
    erdi8_start: str
    erdi8_safe: bool
    fasterid_max_num: int
    fasterid_always_rdf: bool
    fasterid_max_prefix_len: int
    fasterid_property: str
    fasterid_default_prefix: str
    fasterid_store_type: StorageType = StorageType.FILE_LOG
    fasterid_store_loc: str

    class Config:
        env_file = "fasterid.env"
