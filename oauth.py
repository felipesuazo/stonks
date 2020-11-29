from typing import Optional

from authlib.integrations.httpx_client import AsyncOAuth2Client

import settings


class TwitchOauthClient:
    @staticmethod
    def get_client(token: Optional = None):
        params = dict(
            client_id=settings.TWITCH_CLIENT_ID,
            client_secret=settings.TWITCH_CLIENT_SECRET,
            redirect_uri=f'{settings.BASE_URL}/auth/callback',
            scope='chat:read chat:edit user:read:email',
        )

        if token:
            params.update({'token': token})

        return AsyncOAuth2Client(**params)

    @classmethod
    def create_authorization_url(cls):
        return cls.get_client().create_authorization_url(url='https://id.twitch.tv/oauth2/authorize')

    @classmethod
    async def fetch_token(cls, request):
        token_url = f'https://id.twitch.tv/oauth2/token?client_id={settings.TWITCH_CLIENT_ID}&client_secret={settings.TWITCH_CLIENT_SECRET}'
        client = cls.get_client()

        token = await client.fetch_token(
            url=token_url,
            authorization_response=str(request.url),
            grant_type='authorization_code'
        )
        await client.aclose()
        return token

    @classmethod
    async def refresh_token(cls, refresh_token: str):
        token_url = f'https://id.twitch.tv/oauth2/token?client_id={settings.TWITCH_CLIENT_ID}&client_secret={settings.TWITCH_CLIENT_SECRET}&refresh_token={refresh_token}'
        client = cls.get_client()

        token = await client.fetch_token(
            url=token_url,
            grant_type='refresh_token',
        )
        await client.aclose()
        return token

    @classmethod
    async def user_info(cls, token):
        client = cls.get_client(token)
        user = await client.get(
            url='https://api.twitch.tv/helix/users',
            headers={
                'Client-Id': settings.TWITCH_CLIENT_ID,
                'Authorization': f'Bearer {token["access_token"]}'
            }
        )
        await client.aclose()
        return user

