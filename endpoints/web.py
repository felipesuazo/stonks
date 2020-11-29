from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND, HTTP_301_MOVED_PERMANENTLY

from resources import templates
from services import users_services, twitch_services


class Home(HTTPEndpoint):
    async def get(self, request):
        context = {'request': request}

        if request.user.is_authenticated:
            template = 'home_logged.html'
            if request.user.follow_to:
                context.update({'following': request.user.follow_to})
        else:
            template = 'home.html'

        return templates.TemplateResponse(template, context=context)


class Streamer(HTTPEndpoint):
    @requires('authenticated', redirect='home')
    async def get(self, request):
        template = 'streamer.html'
        context = {'request': request}
        return templates.TemplateResponse(template, context=context)

    @requires('authenticated', redirect='home')
    async def post(self, request: Request):
        data = await request.form()

        if "streamer_name" in data and data.get("streamer_name"):
            streamer_name = data.get("streamer_name")
            streamer_exist = await twitch_services.check_streamer_exists(streamer_name)
            if streamer_exist:
                await users_services.set_favorite_streamer(request.user, streamer_name)
                return RedirectResponse(request.url_for('streamer'), status_code=HTTP_302_FOUND)
            return JSONResponse({'error': 'Streamer does not exist'})
        return RedirectResponse(request.url_for('home'), status_code=HTTP_301_MOVED_PERMANENTLY)
