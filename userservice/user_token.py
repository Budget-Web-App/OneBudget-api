from typing import Optional, Any, Dict, Union, List, Iterable

from datetime import datetime, timedelta

import time

import jwt

from cryptography.hazmat.primitives.serialization import load_pem_private_key

from core import logger


class UserToken(jwt.PyJWT):

    pem_private_key = None

    def __init__(self, exp_sec: Union[int, timedelta], email: Optional[str], user_id: Optional[str]):
        super().__init__()

        if isinstance(exp_sec, int):
            exp_sec = self.int_to_expire_time(exp_sec)

        self._email = email or ""
        self._user_id = user_id or ""
        self._issued_at = datetime.utcnow()
        self._expiration_time = self._issued_at + exp_sec

    @staticmethod
    def int_to_expire_time(exp_sec: int) -> timedelta:
        """Converts integer to time delta

        Args:
            exp_sec (int): The number of seconds till token expires

        Returns:
            timedelta: The time delta version of the exp_sec
        """

        return timedelta(seconds=exp_sec)

    @classmethod
    def load_pem_private_key(
        cls, data: bytes, password: Optional[bytes], backend: Any = None
    ) -> None:

        cls.pem_private_key = load_pem_private_key(data, password, backend)

    @classmethod
    def create_user_token(cls, user: Dict[str, Any], exp_sec: int) -> "UserToken":

        email = user["email"]
        userid = user["userid"]

        return cls(exp_sec, email, userid)

    def encode(
        self, key: str, alg="HS256", optional_headers: Optional[Dict[str, str]] = None
    ) -> str:

        payload = {
            "email": self._email,
            "userid": self._user_id,
            "iat": self._issued_at,
            "exp": self._expiration_time,
        }

        private_key = key or self.pem_private_key

        return super().encode(payload, private_key, alg, optional_headers)

    @classmethod
    def decode(cls, raw_token: str, key: str = "", algorithms: Optional[List[str]] = None, options: Optional[Dict[str, Any]] = None, verify: Optional[bool] = None, detached_payload: Optional[bytes] = None, audience: Optional[Union[str, Iterable[str]]] = None, issuer: Optional[str] = None, leeway: Union[int, float, timedelta] = 0, **kwargs) -> Dict[str, Any]:
        
        raw_decoded_token = jwt.decode(raw_token, key=key, algorithms=algorithms, verify=verify)
        
        return cls.from_json(raw_decoded_token)

    @classmethod
    def from_json(cls, decoded_token: Dict[str, Any]) -> 'UserToken':

        token = cls(0, None, None)
        token._email = decoded_token["email"]
        token._user_id = decoded_token["userid"]
        
        token._issued_at = datetime_from_utc_to_local(decoded_token["iat"])

        logger.debug("issued at: %s", token._issued_at)

        token._expiration_time = datetime_from_utc_to_local(decoded_token["exp"])

        return token

def datetime_from_utc_to_local(utc_datetime: int):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return datetime.fromtimestamp(utc_datetime)