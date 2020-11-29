from starlette.applications import Starlette

import settings
from middleware import middleware
from models import *
from routes import routes


def create_app():
    _app = Starlette(
        debug=settings.DEBUG,
        routes=routes,
        middleware=middleware,
    )
    db.init_app(_app)
    return _app


app = create_app()


@app.on_event('startup')
async def create_models():
    await db.gino.create_all()
