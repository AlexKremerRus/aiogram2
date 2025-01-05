from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
import asyncio
import os

# Получаем токен с проверкой
token = os.getenv('TOKEN_API')
if not token:
    raise ValueError("Токен бота не найден. Установите переменную окружения TOKEN_API")

# Инициализация бота и диспетчера
bot = Bot(token=token)
dp = Dispatcher()

# Пример обработчика команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот.")

# Пример обработчика текстовых сообщений
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)

# Функция запуска бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())