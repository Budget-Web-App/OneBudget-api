from shared import generate_new_token, validate_new_user, get_private_key, get_public_key, get_token_data, verify_token
from __init__ import app
from decorators import exception_handler, requires_token, required_args, ArgumentError, SQLLookupError, EndpointPermissionError, CategoryLookupError
from core import logger

from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import bcrypt

import bleach
from werkzeug.utils import secure_filename
from zipfile import ZipFile

def create_app():
    """Flask application factory to create instances
    of the Userservice Flask App
    """

    return app


if __name__ == "__main__":
    # Create an instance of flask server when called directly
    USERSERVICE = create_app()
    USERSERVICE.run(debug=True, use_reloader=True)
