from db import CategoryDb
from decorators import exception_handler, requires_token, required_args, CategoryLookupError
from core import logger

import os
import bleach
from flask import Blueprint, request, jsonify

from user_token import UserToken

categories_api = Blueprint('categories_api', __name__)

categories_db = CategoryDb(os.environ.get("CATEGORIES_DB_URI"), logger)

@categories_api.route('/categories', methods=["GET"])
@exception_handler
@requires_token
def list_user_categories(token: UserToken):

    logger.debug("fetching categories")
    categories = categories_db.list_categories_by_user_id(token._user_id)
    logger.debug("successfully got categories")

    return jsonify({"values": categories}), 201

@categories_api.route('/budgets/<budget_id>/categories', methods=["POST"])
@exception_handler
@requires_token
@required_args('displayname')
def add_budget_category(budget_id: str, token: UserToken, **kwargs):

    raw_parentid = request.args.get('parentid', None, str)

    categoryid = categories_db.generate_categoryid()
    displayname = bleach.clean(kwargs["all_provided_args"]['displayname'])

    parentid = bleach.clean(
        raw_parentid) if raw_parentid is not None else None

    if (parentid is not None) and (categories_db.get_category(parentid) is None):
        raise CategoryLookupError(
            "Unable to find category with Id {0}".format(parentid), 401)

    category_data = {
        "categoryid": categoryid,
        "displayname": displayname,
        "parentid": parentid,
        "budgetid": budget_id,
        "userid": token._user_id
    }

    # Add user_data to database
    logger.debug("Adding category to the database")
    categories_db.add_category(category_data)
    logger.info("Successfully created category.")

    budget = categories_db.get_category(category_data["categoryid"])

    return jsonify(budget), 201

@categories_api.route('/budgets/<budget_id>/categories', methods=["GET"])
@exception_handler
@requires_token
def get_budget_categories(token: UserToken, budget_id: str, **kwargs):

    logger.debug("fetching budget categories")
    categories = categories_db.list_categories_by_budget_id(budget_id)
    logger.debug("successfully got categories")

    return jsonify({"values": categories}), 201
