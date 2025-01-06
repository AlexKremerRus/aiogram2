from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

# Получаем токен из переменной окружения
token = os.getenv('TOKEN_API')

# Инициализация бота и диспетчера
bot = Bot(token)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот.")

# Обработчик текстовых сообщений
@dp.message()
async def echo(message: types.Message):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='hello', callback_data='hello')]
    ])
    await message.answer(message.text, reply_markup=markup)

# Обработчик callback_query
@dp.callback_query(lambda call: call.data == 'hello')
async def callback(call: types.CallbackQuery):
    await call.message.answer("Вы нажали кнопку 'hello'")

async def main():
    # Запуск поллинга
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())

