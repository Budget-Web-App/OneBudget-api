from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

import pyotp

from base64 import b32encode

from bleach import clean
import bcrypt

from sqlalchemy.orm import Session

from ....models import Registration, TokenResponse, Token
from ....models.user import User
from ....db.user import UserDb
from ....internal import get_db

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["oauth"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@oauth_router.get("/authorize")
async def authorize(
    state: bytes,
    redirect_uri: str,
    response_type: Optional[str] = None,
):
    totp: pyotp.TOTP = pyotp.TOTP(
        b32encode(state).decode('utf-8'), interval=600)
    code = totp.now()

    return RedirectResponse(
        url=redirect_uri+f"?code={code}&state={state}"
    )


@oauth_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:

    email = clean(form_data.username)
    password = clean(form_data.password)

    scopes = form_data.scopes

    user: User = UserDb.get_user(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user.pass_hash):
        raise HTTPException(
            status_code=401, detail="email or password is incorrect.")

    # Generates token
    access_token = Token.create_token(user.email, user.id)

    payload = TokenResponse(
        access_token=access_token,
        refresh_token=None,
        token_type="bearer",
        scope=scopes,
    )

    return payload


@oauth_router.post('/refresh')
def refresh(refresh_token: str, db: Session = Depends(get_db)):

    raise HTTPException(status_code=404, detail="refresh endpoint not implemented")


@oauth_router.post("/register")
async def register(registration_info: Registration, db: Session = Depends(get_db)):

    salt = bcrypt.gensalt()
    passhash = bcrypt.hashpw(registration_info.password.encode('utf-8'), salt)

    user = User(
        id = "",
        email=registration_info.email,
        pass_hash=passhash
    )

    try:
        new_user = UserDb.add_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=406, detail=str(e))

    # Generates token
    access_token = Token.create_token(user.email, user.id)

    payload = TokenResponse(
        access_token=access_token,
        refresh_token=None,
        token_type="bearer",
        scope=[],
    )
