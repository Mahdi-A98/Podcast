# In the name of GOD

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Scope, Receive, Message
from fastapi import Request, Response

from services import SERVICE_CLASSES
from utils.async_iterator import async_iterator_wrapper as aiwrap

class InternalSecurityMiddleware(BaseHTTPMiddleware):
