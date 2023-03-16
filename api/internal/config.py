from os import environ
from functools import lru_cache
from dotenv import load_dotenv

from pydantic import BaseSettings

load_dotenv("C:\\Users\\micha_063o0o\\Projects\\OneBudget-api (new)\\api\\internal\\.env")

class Settings(BaseSettings):
    PRIVATE_KEY: bytes
    PUBLIC_KEY: bytes
    SECRET: bytes


@lru_cache()
def get_settings():
    
    return Settings(PRIVATE_KEY=open(environ.get("PRIV_KEY_PATH"), 'rb').read(),PUBLIC_KEY=open(environ.get("PUB_KEY_PATH"), 'rb').read(), SECRET=bytes(environ.get('SECRET'), 'utf-8'))