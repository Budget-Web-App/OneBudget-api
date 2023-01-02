from flask import current_app
from typing import Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
import jwt
from datetime import datetime, timedelta

def verify_token(token):
    """
    Validates token using userservice public key
    """
    current_app.logger.debug('Verifying token.')
    if token is None:
        return False
    try:
        jwt.decode(token, key=get_private_key(),
                    algorithms='RS256', verify=False)
        current_app.logger.debug('Token verified.')
        return True
    except jwt.exceptions.InvalidTokenError as err:
        current_app.logger.error('Error validating token: %s', str(err))
        return False

def get_token_data(token):
    current_app.logger.debug('Getting token data.')
    if token is None:
        return None
    try:
        token = jwt.decode(token, key=get_private_key(),
                               algorithms='RS256', verify=False)
        return token
    except jwt.exceptions.InvalidTokenError as err:
        current_app.logger.error('Error getting token: %s', str(err))
        return None

def get_public_key():
    public_rsakey = load_pem_public_key(current_app.config['PUBLIC_KEY'], backend=default_backend())
    return public_rsakey

def get_private_key():
    priv_rsakey = load_pem_private_key(current_app.config['PRIVATE_KEY'], password=current_app.config['SECRET'], backend=default_backend())
    return priv_rsakey

def validate_new_user(req):
    current_app.logger.debug('validating create user request: %s', str(req))
    # Check if required fields are filled
    fields = (
        'email',
        'password',
    )
    if any(f not in list(req.keys()) for f in fields):
        raise UserWarning('missing required field(s)')
    if any(not bool(req[f] or req[f].strip()) for f in fields):
        raise UserWarning('missing value for input field(s)')

def generate_new_token(user: dict) -> Tuple[bytes, timedelta]:
    exp_sec = timedelta(seconds=current_app.config['EXPIRY_SECONDS'])
    exp_time = datetime.utcnow() + exp_sec
    payload = {
            'email': user["email"],
            'userid': user['userid'],
            'iat': datetime.utcnow(),
            'exp': exp_time,
    }

    # Generate token
    return jwt.encode(payload, get_private_key(), algorithm='RS256'), exp_sec