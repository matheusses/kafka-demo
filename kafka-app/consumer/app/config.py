import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    topics: str
    client_id : str
    group_id : str
    auto_offset_reset : str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> BaseSettings:
    load_dotenv()
    return Settings()
