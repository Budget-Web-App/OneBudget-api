from typing import Optional
from fastapi import FastAPI, Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from bleach import clean
import bcrypt

from sqlalchemy.orm import Session

from .models import Authentication, GrantTypes, Registration, TokenResponse, Token
from .models.user import User
from .routers.beta import beta_router
from .db.user import UserDb
from .internal import get_db

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

@app.get("/authorize")
async def authorize(
    response_type: Optional[str] = None,
    redirect_uri: Optional[str] = None,
):
    pass


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response_type: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> TokenResponse:

    email = clean(form_data.username)
    password = clean(form_data.password)

    user: User = UserDb.get_user(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Generates token
    token, exp_time = Token.create_token(user.email, user.id)

    payload = TokenResponse(access_token=token, token_type="bearer")

    return payload


@app.post("/register")
async def register(registration_info: Registration, db: Session = Depends(get_db)):

    salt = bcrypt.gensalt()
    passhash = bcrypt.hashpw(registration_info.password.encode('utf-8'), salt)

    user = User(
        email=registration_info.email,
        pass_hash=passhash
    )

    new_user = UserDb.add_user(db, user)
