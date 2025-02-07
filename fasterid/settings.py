#!/usr/bin/env python3

# Copyright (C) 2023  Andreas Thalhammer
# Please get in touch if you plan to use this in a commercial setting.

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
    fasterid_id_property: str
    fasterid_ts_property: str
    fasterid_default_prefix: str
    fasterid_store_type: StorageType = StorageType.FILE_LOG
    fasterid_store_loc: str

    class Config:
        env_file = ".env"
