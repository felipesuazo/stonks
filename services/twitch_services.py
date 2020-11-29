import hashlib
import hmac
import uuid
from datetime import datetime

import httpx
from typing import Optional, Any, Dict, List

from sqlalchemy import desc

import constants
import settings
from middleware.context import get_token
from models.event import Event
from models.subscription import Subscription
from oauth import TwitchOauthClient


async def get_subscription_by_id(subscription_id: str) -> Optional[Subscription]:
    return await Subscription.get(subscription_id)


async def get_subscription_by_type_and_streamer(subscription_type: str, streamer_name: str) -> Optional[Subscription]:
    return await Subscription.query.where(
        Subscription.type == subscription_type
    ).where(
        Subscription.broadcaster_user_name == streamer_name
    ).gino.first()


async def get_event_by_id(event_id: str) -> Optional[Event]:
    return await Event.get(event_id)


async def get_last_events_by_streamer(streamer_name: str, event_amount: int = 10) -> List[Dict]:
    events = (
        await Event.query
            .where(Event.streamer_name == streamer_name)
            .order_by(desc(Event.created_at))
            .limit(event_amount)
            .gino.all()
    )
    return [event.as_dict() for event in events]


async def check_streamer_exists(streamer_name: str) -> Optional[Dict]:
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
    return streamer


def check_signature(
    message_id: str, timestamp: str, body: bytes, secret: str, expected: str
) -> bool:
    hmac_message = message_id + timestamp + body.decode('utf-8')
    signature = hmac.new(
        key=secret.encode('utf-8'),
        msg=hmac_message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return f'sha256={signature}' == expected


async def process_notification(
    subscription_type: str, event_data: Any, message_id: str
) -> Event:
    return await Event.create(
        id=message_id,
        streamer_name=event_data['broadcaster_user_name'],
        event_type=subscription_type,
        viewer_name=event_data.get('user_name'),
        created_at=datetime.now()
    )


async def start_events_subscription(streamer_data: Dict) -> None:
    app_credentials = await TwitchOauthClient.get_app_token()
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {app_credentials["access_token"]}'
    }

    subscription_data = {
        'version': '1',
        'condition': {
            'broadcaster_user_id': streamer_data['id']
        },
        'transport': {
            'method': 'webhook',
            'callback': f'{settings.BASE_URL}/twitch_event',
            'secret': str(uuid.uuid4())
        }
    }

    for event in constants.SUBSCRIPTION_TYPES:
        await _start_event_sub(
            subscription_type=event,
            streamer_id=streamer_data['id'],
            streamer_name=streamer_data['display_name'],
            headers=headers,
            subscription_data=subscription_data
        )


async def _start_event_sub(
    subscription_type: str,
    streamer_id: str,
    streamer_name: str,
    headers: Dict,
    subscription_data: Dict
) -> None:
    exists_subscription = await get_subscription_by_type_and_streamer(subscription_type, streamer_name)

    if not exists_subscription:
        url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
        subscription = httpx.post(
            url=url,
            headers=headers,
            json={'type': subscription_type, **subscription_data}
        )
        response_data = subscription.json()['data'][0]

        await Subscription.create(
            id=response_data['id'],
            type=subscription_type,
            secret=subscription_data['transport']['secret'],
            broadcaster_user_name=streamer_name,
            broadcaster_user_id=streamer_id,
        )
