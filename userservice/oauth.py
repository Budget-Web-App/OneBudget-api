from flask import Blueprint, request, jsonify, url_for
import bleach
import bcrypt
import os

# interal imports
from shared import generate_new_token
from decorators import (
    exception_handler,
    requires_token,
    required_args,
    ArgumentError,
    SQLLookupError,
    EndpointPermissionError,
    CategoryLookupError,
)
from db import UserDb
from core import logger

users_db = UserDb(os.environ.get("ACCOUNTS_DB_URI"), logger)

oauth_api = Blueprint("oauth_api", __name__)


@oauth_api.route("/token", methods=["POST"])
@exception_handler
def get_token():
    _grant_type = request.args.get("grant_type")

    json = request.json

    raw_email = json.get("email", None)
    raw_password = json.get("password", None)

    logger.debug("Sanitizing login input.")

    if raw_email is None:
        raise ArgumentError("No email argument provided", 419)

    if raw_password is None:
        raise ArgumentError("No password argument provided", 419)

    remember_me = request.form.get("rememberme", False, bool)

    email = bleach.clean(raw_email)
    password = bleach.clean(raw_password)

    user = users_db.get_user(email)
    if user is None:
        raise SQLLookupError("user {0} does not exist".format(email), 404)

    # Validate the password
    if not bcrypt.checkpw(password.encode("utf-8"), user["passhash"]):
        raise EndpointPermissionError("Invalid login", 401)

    # Generates token
    token, exp_time = generate_new_token(user)

    payload = {
        "token": token.decode("utf-8"),
        "token_type": "bearer",
        "expires_in": exp_time.seconds,
    }

    return jsonify(payload), 200
