from pydantic import BaseSettings

class Settings(BaseSettings):
    erdi8_stride: int
    erdi8_start: str
    erdi8_safe: bool
    fasterid_max_num: int
    fasterid_max_prefix_len: int
    fasterid_filename: str

    class Config:
        env_file = "fasterid.env"
