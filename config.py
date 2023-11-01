import os 
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import admin, client
from module.vosk import Vosk

load_dotenv()
vosk = Vosk("vosk-model-small-ru-0.22")
bot = Bot(token=os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_routers(
    admin.router,
    client.router
)


