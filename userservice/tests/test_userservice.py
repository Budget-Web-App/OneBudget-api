"""
Tests for userservice
"""

import random
import unittest
from unittest.mock import patch, mock_open

from sqlalchemy.exc import SQLAlchemyError
import jwt

from userservice import create_app
from tests.constants import (
    TIMESTAMP_FORMAT,
    EXAMPLE_USER_REQUEST,
    EXAMPLE_USER,
    EXPECTED_FIELDS,
    EXAMPLE_PRIVATE_KEY,
    EXAMPLE_PUBLIC_KEY,
    INVALID_USERNAMES,
)

if __name__ == '__main__':
    app = create_app()
    app.run()