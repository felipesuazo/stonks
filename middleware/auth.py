import json
from datetime import datetime
from typing import Optional, Tuple, Dict

from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response

from models.user import User
from oauth import TwitchOauthClient
from services import users_services
import utils


class CookieAuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, User]]:
        if 'token' in conn.cookies:
            token = json.loads(conn.cookies.get('token'))
            user = json.loads(conn.cookies.get('user'))

            expires_at = datetime.utcfromtimestamp(token['expires_at'])
            refresh_token = token['refresh_token']
            now = datetime.now()

            # Check token expiration
            if expires_at > now:
                token, user = await self._refresh_access_token(refresh_token)
                self._update_auth_cookies(conn, token, user)
            self._add_data_to_session(conn, token, user)

            # Check user in database
            user_model = await self._check_user_in_db(user)

            # Store token and user in global context
            conn.scope['user'] = user
            conn.scope['token'] = token

            return AuthCredentials(['authenticated']), user_model
        return

    @staticmethod
    async def _refresh_access_token(refresh_token: str):
        token = await TwitchOauthClient.refresh_token(refresh_token)
        user = await TwitchOauthClient.user_info(token)
        user = user.json()['data'][0]
        return token, user

    @staticmethod
    def _add_data_to_session(conn, token, user):
        conn.session['X-Data'] = {
            'token': token,
            'user': user
        }

    @staticmethod
    def _update_auth_cookies(conn, token, user):
        conn.session['X-Update-Cookie'] = {
            'token': token,
            'user': user,
        }

    @staticmethod
    async def _check_user_in_db(user_data: Dict) -> User:
        user_id = int(user_data['id'])
        user = await users_services.get_user_by_id(user_id)
        if not user:
            user = await users_services.create_user(user_data)
        else:
            await users_services.update_user(user, user_data)
        return user


class SetCookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if 'X-Update-Cookie' in request.session:
            update_cookies = request.session.pop('X-Update-Cookie')
            if update_cookies:
                utils.set_cookie(response, "token", json.dumps(update_cookies['token']))
                utils.set_cookie(response, "user", json.dumps(update_cookies['user']))
        return response
