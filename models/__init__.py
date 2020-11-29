from gino_starlette import Gino

import settings

db = Gino(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASS,
    database=settings.DB_NAME,
)

__all__ = ['event', 'subscription', 'user', 'db']