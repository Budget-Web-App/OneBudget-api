from typing import Optional

from datetime import datetime, timedelta

from fastapi import HTTPException

from pydantic import BaseModel
from enum import Enum, StrEnum, auto

from api.internal import get_private_key

from jwt import encode, decode, exceptions

class Authentication(BaseModel):
    email: str
    password: str
    
class Registration(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class Token(BaseModel):
    email: str
    user_id: str
    iat: int
    exp: int
    
    @classmethod
    def parse_token(cls, token: str) -> Optional["Token"]:
        """_summary_

        Returns:
            _type_: _description_
        """
        
        if token is None:
            raise HTTPException(status_code=401, detail="Missing Token")

        token = token.replace("Bearer ", "")

        try:
            decoded_token = decode(token, key=get_private_key(), algorithms=[
                                'RS256'], options={"verify_signature": False})
            return Token(**decoded_token)
        except exceptions.InvalidTokenError as err:
            raise HTTPException(status_code=500, detail="Unexpected error parsing token")
    
    @classmethod
    def create_token(cls, email: str, user_id: str) -> str:
        
        exp_sec = timedelta(seconds=10)
        exp_time = datetime.utcnow() + exp_sec
        
        payload = Token(
            email=email,
            user_id=user_id,
            iat=datetime.utcnow(),
            exp=exp_time,
        )
        
        # Generate token
        return encode(payload, get_private_key(), algorithm='RS256')
    
    def encode(self) -> str:
        # Generate token
        return encode(self, get_private_key(), algorithm='RS256')
        
        
class GrantTypes(StrEnum):
    AuthorizationCode = auto()
    ClientCredentials = auto()
    DeviceCode = auto()
    RefreshToken = auto()