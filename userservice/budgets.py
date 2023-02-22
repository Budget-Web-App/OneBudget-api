from typing import Tuple
from requests import Response
import os
import requests
from flask import Blueprint, request, jsonify, url_for
import bleach
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError

# interal imports
from decorators import (
    exception_handler,
    requires_token,
    required_args,
    required_permissions,
    ArgumentError,
    MissingFileError,
    BudgetLookupError,
)
from db import BudgetDb
from core import logger
from user_token import UserToken

budgets_api = Blueprint("budgets_api", __name__, url_prefix="/budgets")

budgets_db = BudgetDb(os.environ.get("BUDGETS_DB_URI"), logger)


@budgets_api.route("/", methods=["POST"])
@exception_handler
@requires_token
def add_users_budgets(token: UserToken):

    user_id = token._user_id

    # get display name from form
    raw_displayname = request.form.get("displayname", None, str)
    # get budget notes from form
    raw_budgetnotes = request.form.get("notes", "", str)

    if raw_displayname is None:
        raise ArgumentError("No display name argument provided", 419)

    budgetid = budgets_db.generate_budgetid()
    budgetnotes = bleach.clean(raw_budgetnotes)
    displayname = bleach.clean(raw_displayname)

    budget_data = {
        "budgetid": budgetid,
        "displayname": displayname,
        "budgetnotes": budgetnotes,
        "accessdate": datetime.utcnow(),
        "userid": user_id,
    }

    # Add user_data to database
    logger.debug("Adding budget to the database")
    budgets_db.add_budget(budget_data)
    logger.info("Successfully created budget.")

    budget = budgets_db.get_budget(budget_data["budgetid"])

    return jsonify(budget), 201


@budgets_api.route("/", methods=["GET"])
@exception_handler
@requires_token
def get_users_budgets(token: UserToken):
    try:
        user_id = token._user_id
        # Get all budgets that belong to this user
        logger.debug("fetching budgets of %s", user_id)
        budgets = budgets_db.get_budgets(user_id)
        logger.debug("successfully got budgets")

        dict_return = {"values": budgets}

        return jsonify(dict_return), 200

    except SQLAlchemyError as err:
        logger.error("Error fetching budgets: %s", str(err))
        return "failed to fetch budgets", 500


# Needs work
@budgets_api.route("/upload", methods=["POST"])
@exception_handler
def upload_budget(token: UserToken):

    user_id = token._user_id

    file = request.files["file"]
    if file.filename == "":
        raise MissingFileError("No file selected for uploading", 400)

    filename = secure_filename(file.filename)


@budgets_api.route("/<budget_id>", methods=["GET"])
@exception_handler
@requires_token
def get_users_budget(token: UserToken, budget_id: str):

    try:
        user_id = token._user_id
        # Get all budget with the specified id
        logger.debug("fetching budget with id of %s", budget_id)
        budget = budgets_db.get_budget(budget_id)
        logger.debug("successfully got budget")

        category_URL = "http://localhost:5000/{0}".format(
            url_for(
                "categories_api.get_budget_categories",
                budget_id=budget_id,
                user_id=user_id,
            )
        )
        categories = requests.get(url=category_URL, headers=request.headers)

        categories_json = categories.json()

        logger.debug(categories_json)

        budget["categories"] = categories_json["values"]

        return jsonify(budget), 201

    except SQLAlchemyError as err:
        logger.error("Error fetching budgets: %s", str(err))
        return "failed to fetch budgets", 500


@budgets_api.route("/<budget_id>", methods=["PATCH"])
@exception_handler
@requires_token
def update_users_budget(token: UserToken, budget_id: str):

    try:
        user_id = token._user_id
        req = {k: bleach.clean(v) for k, v in request.form.items()}
        req["budgetid"] = budget_id
        req["accessdate"] = datetime.utcnow()

        if budgets_db.get_budget(req["budgetid"]) is None:
            raise LookupError("budget with id {0} not found".format(req["budgetid"]))

        logger.debug("Updating budget with id %s", req["budgetid"])
        budgets_db.update_budget(req)
        logger.debug("Successfully updated budget")

        budget = budgets_db.get_budget(req["budgetid"])

        return jsonify(budget), 201

    except LookupError as err:
        logger.error("Error updating budget: %s", str(err))
        return str(err), 404

    except SQLAlchemyError as err:
        logger.error("Error creating new user: %s", str(err))
        return "failed to update budget", 500


@budgets_api.route("/<budget_id>", methods=["DELETE"])
@exception_handler
@requires_token
def remove_users_budget(token: UserToken, budget_id: str) -> Tuple[Response, int]:
    """Removes the specified budget for the specified user

    Args:
        user_id (str): Id of the user who owns the budget
        budget_id (str): Id of the budget

    Returns:
        Tuple[Response, int]: _description_
    """

    user_id = token._user_id

    if budgets_db.get_budget(budget_id) is None:
        raise BudgetLookupError("budget with id {0} not found".format(budget_id), 404)

    logger.debug("Deleting budget with id %s", budget_id)
    budgets_db.delete_budget(budget_id)
    logger.debug("Successfully deleted budget")

    return jsonify({}), 201
