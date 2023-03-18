from os import environ
from functools import lru_cache
from dotenv import load_dotenv

from fastapi_jwt_auth import AuthJWT

from pydantic import BaseSettings

load_dotenv("C:\\Users\\micha_063o0o\\Projects\\OneBudget-api\\api\\internal\\.env")

class Settings(BaseSettings):
    authjwt_private_key: str
    authjwt_public_key: str
    authjwt_secret_key: str


#@lru_cache()
@AuthJWT.load_config
def get_settings():
    
    return Settings(authjwt_private_key=open(environ.get("PRIV_KEY_PATH"), 'r').read(),authjwt_public_key=open(environ.get("PUB_KEY_PATH"), 'r').read(), authjwt_secret_key=environ.get('SECRET'))