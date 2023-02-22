from flask import Blueprint, request, jsonify, url_for
import bleach
import bcrypt
import os

from sqlalchemy.exc import SQLAlchemyError

from shared import generate_new_token, validate_new_user
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

@oauth_api.route("/signup", methods=["POST"])
@exception_handler
def signup():
    try:
        logger.debug('Sanitizing input.')
        req = {k: bleach.clean(v) for k, v in request.form.items()}
        validate_new_user(req)

        if users_db.get_user(req["email"]) is not None:
            raise LookupError(
                "email {0} is already in use".format(req["email"]))

        accountid = users_db.generate_userid()

        logger.debug('generating password hash')
        password = req["password"]
        salt = bcrypt.gensalt()
        passhash = bcrypt.hashpw(password.encode('utf-8'), salt)
        logger.info('Successfully generated password hash')

        user_data = {
            "userid": accountid,
            "email": req["email"],
            "timezone": req["timezone"],
            "passhash": passhash
        }

        # Add user_data to database
        logger.debug("Adding user to the database")
        users_db.add_user(user_data)
        logger.info("Successfully created user.")

        user = users_db.get_user(user_data["email"])
        del user["passhash"]

        return jsonify(user), 201
    except UserWarning as warn:
        logger.error("Error creating new user: %s", str(warn))
        return str(warn), 400
    except NameError as err:
        logger.error("Error creating new user: %s", str(err))
        return str(err), 409
    except SQLAlchemyError as err:
        logger.error("Error creating new user: %s", str(err))
        return 'failed to create user', 500
    except Exception as e:
        return str(e), 404