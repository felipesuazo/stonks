import hashlib
import hmac
import httpx
from typing import Optional, Any

import settings
from middleware.context import get_token
from models.event import Event
from models.subscription import Subscription


async def get_subscription_by_id(subscription_id: str) -> Optional[Subscription]:
    return await Subscription.get(subscription_id)


async def get_event_by_id(event_id: str) -> Optional[Event]:
    return await Event.get(event_id)


async def check_streamer_exists(streamer_name: str) -> bool:
    url = f'https://api.twitch.tv/helix/users?login={streamer_name}'
    token = get_token()
    headers = {
        'Authorization': f"Bearer {token['access_token']}",
        'Client-Id': settings.TWITCH_CLIENT_ID
    }
    streamer_request = httpx.get(
        url=url,
        headers=headers
    )
    streamer = next(iter(streamer_request.json()['data']), None)
    return streamer is not None


def check_signature(
    message_id: str, timestamp: str, body: str, secret: str, expected: str
) -> bool:
    hmac_message = message_id + timestamp + body
    signature = hmac.new(
        key=bytes(secret),
        msg=bytes(hmac_message),
        digestmod=hashlib.sha256
    )
    return str(signature) == expected


async def process_notification(
    subscription_type: str, event_data: Any
):
    pass