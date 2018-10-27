from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode, Message
from aiohttp import BasicAuth
from app.conf import TOKEN, PROXY, PROXY_LOGIN, PROXY_PASSWORD
import logging

logging.basicConfig(level=logging.INFO)


bot = Bot(TOKEN, parse_mode=ParseMode.HTML, proxy=PROXY,
          proxy_auth=BasicAuth(login=PROXY_LOGIN, password=PROXY_PASSWORD))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: Message):
    await bot.send_message(message.from_user.id, 'hi')
