from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')
BOT_TOKEN = getenv('BOT_TOKEN')
BASE_URL = getenv('BASE_URL')

SQLALCHEMY_DATABASE_URI = 'sqlite:///app_db.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True