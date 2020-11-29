from starlette import status
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

import constants
from services import twitch_services


class Callback(HTTPEndpoint):
    async def post(self, request: Request):
        try:
            message_id = request.headers['Twitch-Eventsub-Message-Id']
            retry = int(request.headers['Twitch-Eventsub-Message-Retry'])
            event_type = request.headers['Twitch-Eventsub-Message-Type']
            signature = request.headers['Twitch-Eventsub-Message-Signature']
            timestamp = request.headers['Twitch-Eventsub-Message-Timestamp']
            subscription_type = request.headers['Twitch-Eventsub-Subscription-Type']
            subscription_version = request.headers['Twitch-Eventsub-Subscription-Version']
        except KeyError:
            return JSONResponse({'error': 'Header key is missing'})

        event_data = await request.json()
        subscription = await twitch_services.get_subscription_by_id(
            subscription_id=event_data['subscription']['id']
        )

        if subscription and twitch_services.check_signature(
            message_id=message_id,
            timestamp=timestamp,
            body=await request.body(),
            secret=subscription.secret,
            expected=signature
        ):
            if event_type == constants.EVENT_WEBHOOK_CALLBACK_VERIFICATION:
                print(event_data)
                return PlainTextResponse(
                    status_code=status.HTTP_200_OK,
                    content=event_data['challenge']
                )
            elif event_type == constants.EVENT_NOTIFICATION:
                event = await twitch_services.get_event_by_id(message_id)
                if not event:
                    await twitch_services.process_notification(
                        subscription_type=subscription_type,
                        event_data=event_data['event'],
                        message_id=message_id
                    )
                return JSONResponse(status_code=status.HTTP_200_OK)

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'error': 'No subscription found or invalid signature'})
