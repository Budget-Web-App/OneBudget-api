from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi_jwt_auth import AuthJWT

from bleach import clean
import bcrypt

from sqlalchemy.orm import Session

from .models import Authentication, GrantTypes, Registration, TokenResponse, Token
from .models.user import User
from .routers.beta import beta_router
from .db.user import UserDb
from .internal import get_db, jwt_refresh_token_required

app = FastAPI(
    debug=True,
    title="OneBudget",
    description="",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(beta_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
