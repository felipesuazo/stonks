from starlette.routing import Route, Mount, WebSocketRoute

from endpoints import web, twitch, auth
from resources import assets

routes = [
    Route('/', web.Home, name='home'),
    Route('/streamer', web.Streamer, name='streamer'),
    Route('/twitch_event', twitch.Callback, name='twitch_event'),
    Route('/auth', auth.Auth, name='auth'),
    Route('/auth/callback', auth.Callback, name='auth_callback'),
    WebSocketRoute('/ws', web.StreamerEvents, name='ws_events'),
    Mount('/assets', assets, name='assets'),
]
