import json
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

import constants

_ctx_token_var: ContextVar = ContextVar(constants.CTX_TOKEN_KEY, default=None)
_ctx_user_var: ContextVar = ContextVar(constants.CTX_USER_KEY, default=None)


def get_token():
    return _ctx_token_var.get()


def get_user():
    return _ctx_user_var.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if 'X-Data' in request.session:
            data = request.session.pop('X-Data')
            if data:
                _ctx_token_var.set(data['token'])
                _ctx_user_var.set(data['user'])
        return await call_next(request)
