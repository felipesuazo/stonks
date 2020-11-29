from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from models.follow_room import FollowRoom


class FollowRoomMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.user.is_authenticated and request.scope['type'] in ('lifespan', 'http', 'websocket'):
            request.scope['room'] = FollowRoom(request.user.follow_to)
        return await call_next(request)
