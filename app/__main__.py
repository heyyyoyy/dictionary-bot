from aiogram.utils.executor import start_polling
from .handlers import dp


if __name__ == '__main__':
    start_polling(dp)
