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
    authjwt_algorithm: str
    authjwt_private_key: str
    authjwt_public_key: str


DATABASE_PATH = environ.get('DB_URI', None)

if DATABASE_PATH is None:
    raise Exception("Env not setup")


@lru_cache
def get_settings():

    PRIV_KEY_PATH = environ.get("PRIV_KEY_PATH")
    PUB_KEY_PATH = environ.get("PUB_KEY_PATH")

    if PRIV_KEY_PATH is None:
        raise Exception("Missing PRIV_KEY_PATH")

    if PUB_KEY_PATH is None:
        raise Exception("Missing PUB_KEY_PATH")

    return Settings(
        authjwt_algorithm="RS512",
        authjwt_private_key=open(PRIV_KEY_PATH, 'r').read(),
        authjwt_public_key=open(PUB_KEY_PATH, 'r').read(),
    )
