import base64
import json

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse

import utils
from oauth import TwitchOauthClient


class Auth(HTTPEndpoint):
    async def get(self, request: Request):
        uri, state = TwitchOauthClient.create_authorization_url()
        return RedirectResponse(uri)


class Callback(HTTPEndpoint):
    async def get(self, request: Request):
        token = await TwitchOauthClient.fetch_token(request=request)
        user = await TwitchOauthClient.user_info(token=token)

        b_token = json.dumps(token)
        b_user = json.dumps(user.json()['data'][0])

        response = RedirectResponse(request.url_for('home'))
        utils.set_cookie(response, "token", b_token)
        utils.set_cookie(response, "user", b_user)
        return response
