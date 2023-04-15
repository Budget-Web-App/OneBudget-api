from os import environ, getcwd
from os.path import join

from functools import lru_cache
from dotenv import load_dotenv

from pydantic import BaseSettings

# To make runnable without docker
if not environ.get("DOCKERCONTAINER", False):
    # To make compatible with any OS
    env_path = join(getcwd(), ".env")

    load_dotenv(env_path)


class Settings(BaseSettings):
    """
    Settings
    ========
    API Settings
    """
    
    authjwt_algorithm: str
    authjwt_private_key: str
    authjwt_public_key: str


DATABASE_PATH = environ.get('DB_URI', None)

if DATABASE_PATH is None:
    raise Exception("Env not setup")


@lru_cache
def get_settings() -> Settings:

    priv_key_path = environ.get("PRIV_KEY_PATH")
    pub_key_path = environ.get("PUB_KEY_PATH")

    if priv_key_path is None:
        raise Exception("Missing PRIV_KEY_PATH")

    if pub_key_path is None:
        raise Exception("Missing PUB_KEY_PATH")

    return Settings(
        authjwt_algorithm="RS512",
        authjwt_private_key=open(priv_key_path, 'r').read(),
        authjwt_public_key=open(pub_key_path, 'r').read(),
    )
