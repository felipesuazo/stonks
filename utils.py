from starlette.responses import Response

import settings


def set_cookie(response: Response, key: str, value: str, expiration: int = 7*24*60*60):
    domain = settings.HOST
    samesite = 'Strict'
    secure = settings.SECURE
    httponly = True

    response.set_cookie(
        key=key,
        value=value,
        domain=domain,
        samesite=samesite,
        secure=secure,
        httponly=httponly,
        max_age=expiration
    )