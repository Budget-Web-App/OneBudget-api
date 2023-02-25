from email import header
from .decorators import exception_handler, requires_token, required_args, ArgumentError, MissingFileError, BudgetLookupError
from db import BudgetDb
from core import logger

import os
import requests
from flask import Blueprint, request, jsonify, url_for
import bleach
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError

months_api = Blueprint('months_api', __name__)

budgets_db = BudgetDb(os.environ.get("BUDGETS_DB_URI"), logger)

@months_api.route("/<user_id>/budgets/<budget_id>/months", methods=["GET"])
@exception_handler
@requires_token
def get_budget_months(user_id: str, budget_id: str):
    pass