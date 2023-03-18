from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_jwt_auth import AuthJWT

import pyotp

from base64 import b32encode

from bleach import clean
import bcrypt

from sqlalchemy.orm import Session

from ....models import Registration, TokenResponse
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
    Authorize: AuthJWT = Depends(),
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
    # token = Token.create_token(user.email, user.id)
    access_token = Authorize.create_access_token(
        subject=user.email,
        user_claims={
            "email": user.email,
            "user_id": user.id
        }
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user.email,
        user_claims={
            "email": user.email,
            "user_id": user.id,
            "scopes": scopes
        }
    )

    payload = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        scope=scopes,
    )

    return payload


@oauth_router.post('/refresh')
def refresh(refresh_token: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):

    if refresh_token is None:
        raise HTTPException(
            status_code=400, detail="Missing refresh_token parameter")

    email: str = Authorize.get_jwt_subject()

    user: User = UserDb.get_user(db, email)

    access_token = Authorize.create_access_token(subject=user.email, user_claims={
                                                 "email": user.email, "user_id": user.id})
    refresh_token = Authorize.create_refresh_token(
        subject=user.email, user_claims={"email": user.email, "user_id": user.id})

    payload = TokenResponse(access_token=access_token,
                            refresh_token=refresh_token, token_type="bearer")

    return payload


@oauth_router.post("/register")
async def register(registration_info: Registration, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):

    salt = bcrypt.gensalt()
    passhash = bcrypt.hashpw(registration_info.password.encode('utf-8'), salt)

    user = User(
        email=registration_info.email,
        pass_hash=passhash
    )

    try:
        new_user = UserDb.add_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=406, detail=str(e))

    access_token = Authorize.create_access_token(subject=user.email, user_claims={
                                                 "email": user.email, "user_id": user.id})
    refresh_token = Authorize.create_refresh_token(
        subject=user.email, user_claims={"email": user.email, "user_id": user.id})

    payload = TokenResponse(access_token=access_token,
                            refresh_token=refresh_token, token_type="bearer")

    return payload
