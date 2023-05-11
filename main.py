"""
License Goes Here
"""
from typing import Callable

import time
import logging.config

from os import environ

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from fastapi_pagination import add_pagination

from api.routers.beta import beta_router

class AccessLogRecord(logging.LogRecord):
    """
    Access Log Record
    =================
    Specialized logging record for the CustomAccessLogFormatter
    """

    remote_addr: str
    request_method: str
    path: str
    http_version: str
    status_code: str
    response_size: str
    referrer: str
    user_agent: str

class CustomAccessLogFormatter(logging.Formatter):
    """
    Custom Access Log Formatter
    ===========================
    Used to format access logs for HTTP requests
    """

    def format(self, record: AccessLogRecord) -> str:
        """Formates the record to the needed log line

        Args:
            record (_type_): _description_

        Returns:
            str: The formatted log line
        """

        timestamp = time.strftime('%d/%b/%Y:%H:%M:%S %z', time.localtime(record.created))
        log_line = f'{record.remote_addr} - [{timestamp}] "{record.request_method} {record.path} {record.http_version}" {record.status_code} {record.response_size} "{record.referrer}" "{record.user_agent}"'
        return log_line

logger = logging.getLogger('access_log')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(CustomAccessLogFormatter())
logger.addHandler(handler)

class AccessLogMiddleware(BaseHTTPMiddleware):
    """
    Access Log Middleware
    =====================
    Middleware for logging HTTP request
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], None]
    ):
        response = await call_next(request)
        log_data = {
            'remote_addr': request.client.host,
            'request_method': request.method,
            'path': request.url.path,
            'http_version': f'HTTP/{request.scope["http_version"]}',
            'status_code': response.status_code,
            'response_size': response.headers.get('content-length', '-'),
            'referrer': request.headers.get('referer', '-'),
            'user_agent': request.headers.get('user-agent', '-')
        }
        logger.info('', extra=log_data)
        return response

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

add_pagination(app)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AccessLogMiddleware)

app.include_router(beta_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
