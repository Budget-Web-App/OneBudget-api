"""
License Here
"""
import logging
import time
from hvac import Client
from os import environ
from os.path import exists
from api.app_logger import get_logger

logger = get_logger(__name__, logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

client = Client(
    url=environ.get("VAULT_ADDR"),
)

# Wait for needed secrets to be created/added
while (not exists("/secret/APP_ROLE_ID") or not exists("/secret/APP_ROLE_SECRET")):
    logger.debug("Waiting until '/secret' directory exists")
    time.sleep(5)

# Set APP_ROLE_ID
with open("/secret/APP_ROLE_ID", "r") as app_role_id:
    environ["APP_ROLE_ID"] = app_role_id.read()
    logger.debug("'APP_ROLE_ID' was successfully set")

# Set APP_ROLE_SECRET
with open("/secret/APP_ROLE_SECRET", "r") as app_role_secret:
    environ["APP_ROLE_SECRET"] = app_role_secret.read()
    logger.debug("'APP_ROLE_SECRET' was successfully set")

#client.auth.approle.login(
#    role_id=environ.get("APP_ROLE_ID"),
#    secret_id=environ.get("APP_ROLE_SECRET"),
#)
