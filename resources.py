from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import settings

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
assets = StaticFiles(directory=str(settings.ASSETS_DIR))
