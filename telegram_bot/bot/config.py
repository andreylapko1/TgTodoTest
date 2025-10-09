import os
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from .api_client import DjangoAPIClient
from .api_client import DjangoAPIClient
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='bot_logs.log'

)


BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')
API_CLIENT = DjangoAPIClient()
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML) )
dp = Dispatcher()