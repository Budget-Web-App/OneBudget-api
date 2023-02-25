from .shared import verify_token, get_token_data
from .core import logger

from flask import request, jsonify

class APIException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.code = error_code


class TokenError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class ArgumentError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class EndpointPermissionError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class MissingFileError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class SQLLookupError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class CategoryLookupError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)


class BudgetLookupError(APIException):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)

def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_code = getattr(e, "code", 500)
            message = getattr(e, "message", "Uknown exception {0}".format(str(e)))
            logger.exception("API exception: %s", message)
            error_response = {
                    "message": message,
                    "error_code": error_code,
            }
            return jsonify(error_response), error_code
    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper

def requires_token(func):
    """Used to check if the path has a token

    Args:
        func (function): _description_
    """
    def _requires_header_token(*args, **kwargs):
        try:
            #app.config['TOKEN_NAME']
            raw_token = request.headers.get("token")

            if raw_token is None:
                raise TokenError("No token provided", 401)

            # Encodes token for verification
            token = raw_token.encode('utf8')

            if not verify_token(token):
                raise UserWarning("user is not authenticated")
            
            kwargs["token"] = get_token_data(token)

            return func(*args, **kwargs)
        except UserWarning as e:
            logger.error("Error validating token: %s", str(e))
            return str(e), 401
    # Renaming the function name:
    _requires_header_token.__name__ = func.__name__
    return _requires_header_token

def validate_args(allowed_args: list):
    def decorator(func):
        def _validate_args(*args, **kwargs):

            kwargs["all_provided_args"] = request.args

            if any(arg not in allowed_args for arg in list(kwargs["all_provided_args"].keys())):
                raise ArgumentError('Unaccepted argument(s) for provided', 420)

            return func(*args, **kwargs)
        # Renaming the function name:
        decorator.__name__ = func.__name__
        return _validate_args
    # Renaming the function name:
    validate_args.__name__ = decorator.__name__
    return decorator

def required_args(require_args: list):
    def required_args_decorator(func):
        def _required_args(*args, **kwargs):

            kwargs["all_provided_args"] = request.args

            # Checks if required args are in list
            if not any(req_arg not in list(kwargs["all_provided_args"].keys()) for req_arg in require_args) or len(kwargs["all_provided_args"]) == 0:
                raise ArgumentError('Missing required argument(s)', 419)

            return func(*args, **kwargs)
        # Renaming the function name:
        _required_args.__name__ = func.__name__
        return _required_args
    # Renaming the function name:
    required_args.__name__ = required_args_decorator.__name__
    return required_args_decorator
