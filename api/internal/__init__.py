from typing import Tuple, Optional
from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

from jwt import encode, decode, exceptions

from .config import get_settings
from ..db import SessionLocal

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_private_key():
    """Gets the private key for JWT token

    Returns:
        _type_: The private key for JWT token
    """

    return load_pem_private_key(get_settings().PRIVATE_KEY, password=get_settings().SECRET, backend=default_backend())


def get_public_key():
    return load_pem_public_key(get_settings().PUBLIC_KEY, backend=default_backend())
