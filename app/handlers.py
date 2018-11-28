from aiogram import Bot, Dispatcher, md
from aiogram.types import ParseMode, Message
from aiohttp import BasicAuth
from .async_parser import Scrapper
from .conf import TOKEN, PROXY, PROXY_LOGIN, PROXY_PASSWORD
import logging

logging.basicConfig(level=logging.INFO)


bot = Bot(TOKEN, parse_mode=ParseMode.HTML, proxy=PROXY,
          proxy_auth=BasicAuth(login=PROXY_LOGIN, password=PROXY_PASSWORD))
dp = Dispatcher(bot)


@dp.errors_handler()
async def error(update, error):
    logging.exception(f'{update}\n')


@dp.message_handler(commands='start')
async def welcome(message: Message):
    await bot.send_message(
        message.from_user.id,
        f'Напиши {md.hcode("/tr word")} чтобы увидеть результат')


@dp.message_handler(commands='tr')
async def translate(message: Message):
    command, *word = message.text.split()
    if word:
        word = word[0]
        scrapper = Scrapper(word)
        await bot.send_message(message.from_user.id, await scrapper.run())
    else:
        await bot.send_message(message.from_user.id, 'Ты не написал слово')
