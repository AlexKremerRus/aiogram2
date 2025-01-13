from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '6643255580:AAF6aap6KvQPfstJsy6vaNpAf6rH2aZyeE8'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

async def send_photo_echo(message: Message):
    if message.photo:
        await message.reply_photo(message.photo[0].file_id)

async def send_document_echo(message: Message):
    if message.document:
        await message.answer_document(message.document.file_id)

async def send_sticker_echo(message: Message):
    if message.sticker:
        await message.answer_sticker(message.sticker.file_id)

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
async def send_echo(message: Message):
    if message.text:
        await message.reply(text=message.text)
    else:
        await message.reply(text="Это не текстовое сообщение")

# Регистрируем хэндлеры
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
dp.message.register(send_document_echo, F.content_type == ContentType.DOCUMENT)
dp.message.register(send_sticker_echo, F.content_type == ContentType.STICKER)
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)