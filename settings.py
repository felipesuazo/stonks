from pathlib import Path

from starlette.config import Config

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
BASE_URL = config('BASE_URL', cast=str)
BASE_DIR = Path(__file__).parent

SECRET_KEY = config('SECRET_KEY', cast=str, default="ix13489245h9dfh9b29j9djafajfawer9234j29")
SECURE = config('SECURE', cast=bool, default=False)
HOST = config('HOST', cast=str)
TEMPLATES_DIR = BASE_DIR / 'templates'
ASSETS_DIR = BASE_DIR / 'assets'

TWITCH_CLIENT_ID = config('TWITCH_CLIENT_ID', cast=str)
TWITCH_CLIENT_SECRET = config('TWITCH_CLIENT_SECRET', cast=str)

DB_HOST = config('DB_HOST', cast=str)
DB_PORT = config('DB_PORT', cast=int)
DB_NAME = config('DB_NAME', cast=str)
DB_USER = config('DB_USER', cast=str)
DB_PASS = config('DB_PASS', cast=str)
