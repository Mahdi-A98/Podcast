# In the name of GOD

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Scope, Receive, Message
from fastapi import Request, Response

from services import SERVICE_CLASSES
from utils.async_iterator import async_iterator_wrapper as aiwrap

class InternalSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # decrypte body of internal services requests
        self.current_request = request
        await self.decrypte_internal_requests(request)
        response = await call_next(request)
        response = await self.encrypte_internal_response(request, response)
        return response
