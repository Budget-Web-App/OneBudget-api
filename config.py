"""
License Goes Here
"""
from os import environ, getcwd
from os.path import join

from functools import lru_cache
from dotenv import load_dotenv

from pydantic import BaseSettings

from api.vault import client

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

DATABASE_PATH = environ.get("DB_URI") #client.read(path="projects-api/database/config/projects-database")

if DATABASE_PATH is None:
    raise Exception("Env not setup") # pylint: disable=broad-exception-raised


@lru_cache
def get_settings() -> Settings:
    """Gets the settings

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        Settings: The settings
    """

    priv_key_path = environ.get("PRIV_KEY_PATH")
    pub_key_path = environ.get("PUB_KEY_PATH")

    if priv_key_path is None:
        raise Exception("Missing PRIV_KEY_PATH")  # pylint: disable=broad-exception-raised

    if pub_key_path is None:
        raise Exception("Missing PUB_KEY_PATH")  # pylint: disable=broad-exception-raised

    with open(priv_key_path, 'r') as priv_file: # pylint: disable=unspecified-encoding
        authjwt_private_key = priv_file.read()

    with open(pub_key_path, 'r') as pub_file: # pylint: disable=unspecified-encoding
        authjwt_public_key = pub_file.read()

    return Settings(
        authjwt_algorithm="RS512",
        authjwt_private_key=authjwt_private_key,
        authjwt_public_key=authjwt_public_key,
    )
