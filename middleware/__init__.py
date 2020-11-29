from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware

import settings
from middleware.auth import CookieAuthBackend, SetCookieMiddleware
from middleware.context import RequestContextMiddleware

middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    Middleware(AuthenticationMiddleware, backend=CookieAuthBackend()),
    Middleware(SetCookieMiddleware),
    Middleware(RequestContextMiddleware)
]
