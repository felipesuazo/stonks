from typing import Set

from starlette.websockets import WebSocket

from models.event import Event


class FollowRoom:
    def __init__(self, streamer_name: str):
        self._streamer_name = streamer_name
        self._websockets: Set[WebSocket] = set()

    def add_websocket(self, websocket: WebSocket):
        if websocket not in self._websockets:
            self._websockets.add(websocket)

    async def broadcast_event(self, event: Event):
        for websocket in self._websockets:
            await websocket.send_json(event.as_dict())

    def remove_websocket(self, websocket: WebSocket):
        del self._websockets[websocket]
