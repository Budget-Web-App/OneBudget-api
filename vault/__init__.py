"""
License Here
"""

from hvac import Client
from os import environ

client = Client(
    url=environ.get("VAULT_ADDR"),
)

client.auth.approle.login(
    role_id='projects-api-role',
#    secret_id='<some_secret_id>',
)

print(client.read(path="projects-api/database/config/projects-database"))
