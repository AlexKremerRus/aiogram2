import sys
import telebot
import os
from telebot import types
from loguru import logger
import sqlite3


# Удаляем стандартный обработчик
logger.remove()
API_wealth = '3d9de74844d28377e81415151cbe6a66'
# Добавляем вывод в консоль
logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
# Добавляем запись в файл
logger.add("debug.log", 
          format="{time} {level} {message}",
          level="DEBUG",
          rotation="10 MB",
          encoding="utf-8")

# Тестовый лог при запуске
logger.debug("====== Бот запускается ======")

token = os.getenv('TOKEN_API')

bot = telebot.TeleBot(token)

name = None
def save(callback):
    logger.debug('====== Начало функции save ======')
    message = callback.message.reply_to_message
    content_type = message.content_type
    
    logger.debug(f"Content type: {content_type}")
    
    # Определяем тип контента и получаем file_id
    if content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_ext = '.jpg'
        save_dir = 'photos'
    elif content_type == 'video':
        file_id = message.video.file_id
        file_ext = '.mp4'
        save_dir = 'videos'
    elif content_type == 'audio':
        file_id = message.audio.file_id
        file_ext = '.mp3'
        save_dir = 'audios'
    elif content_type == 'voice':
        file_id = message.voice.file_id
        file_ext = '.ogg'
        save_dir = 'voices'
    else:
        logger.warning(f"Неподдерживаемый тип контента: {content_type}")
        bot.answer_callback_query(callback.id, f"Тип файла не определен: {content_type}")
        return

    logger.info(f"Попытка сохранения файла. ID: {file_id}")

    try:
        # Получаем информацию о файле
        file_info = bot.get_file(file_id)
        logger.debug(f"Получена информация о файле: {file_info}")
        
        # Скачиваем файл
        downloaded_file = bot.download_file(file_info.file_path)
        logger.debug(f"Файл загружен, размер: {len(downloaded_file)} байт")
        
        # Создаем директорию если её нет
        os.makedirs(save_dir, exist_ok=True)
        
        # Сохраняем файл
        save_path = f'{save_dir}/{file_id}{file_ext}'
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        logger.success(f"Файл успешно сохранен: {save_path}")
        bot.answer_callback_query(callback.id, f"Файл успешно сохранен в папку {save_dir}!")
        
    except Exception as e:
        logger.exception(f"Ошибка при сохранении файла: {str(e)}")
        bot.answer_callback_query(callback.id, f"Ошибка при сохранении: {str(e)}")

def all(message):
     bot.send_message(message.chat.id, 'all')

@bot.message_handler(commands=['start'])
def main(message):
    
    logger.debug('====== Старт прилодения ======')

    conn = sqlite3.connect('test.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup()
    btn_all = types.KeyboardButton('ВСЕ ТОВАРЫ')
    btn_price = types.KeyboardButton('ЦЕНЫ')
    markup.row(btn_all, btn_price)
    bot.send_message(message.chat.id, 'hi, input your name', reply_markup=markup)
    bot.register_next_step_handler(message, user_name)

def on_click(message):
    if message.text == 'ВСЕ ТОВАРЫ':
        all(message)
       
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'input pass')
    bot.register_next_step_handler(message, password)

def password(message):
     
    pass_ = message.text.strip()
    conn = sqlite3.connect('test.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, pass_))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('список пользователей', callback_data='list_persons'))
    bot.send_message(message.chat.id, 'Пользлватель зарегистрирован', reply_markup=markup)


@bot.message_handler(commands=['weather'])
def weathr(message):
    bot.send_message(message.chat.id, 'привет введите название города пожалуйста')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()




@bot.callback_query_handler(func=lambda call: True)
def calback(call):
    conn = sqlite3.connect('test.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    info = ''

    for el in users:
        info+=f"Name: {el[1]} \n"


    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

@bot.message_handler(commands=['test'])
def test_logger(message):
    logger.debug("Тестовый лог - DEBUG")
    logger.info("Тестовый лог - INFO")
    logger.warning("Тестовый лог - WARNING")
    logger.error("Тестовый лог - ERROR")
    bot.reply_to(message, "Тестовые логи записаны")

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

# Обработка по типу и создаем кнопки 
@bot.message_handler(content_types=['photo']) #, 'video', 'audio', 'voice'
def get_method(message):
    logger.debug('====== Получено медиа-сообщение ======')
    markup = types.InlineKeyboardMarkup()
    btn_save = types.InlineKeyboardButton('Save', callback_data='save')
    btn_delete = types.InlineKeyboardButton('Delete', callback_data='delete')
    markup.row(btn_save, btn_delete)
    
    
    logger.debug(f'Тип контента: {message.content_type}')
    if message.content_type == 'photo':
       
        bot.reply_to(message, 'Классное фото!', reply_markup=markup)
    elif message.content_type == 'video':
        bot.reply_to(message, 'Интересное видео!', reply_markup=markup)
    elif message.content_type == 'audio':
        bot.reply_to(message, 'Отличное аудио!', reply_markup=markup)
    elif message.content_type == 'voice':
        bot.reply_to(message, 'Получил ваше голосовое сообщение!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: not None)
def callback_message(call):
    logger.debug('====== Получен callback ======')
    logger.debug(f'Тип callback: {call.data}')
    
    if call.data == 'save':
        logger.debug('Вызываем функцию save')
        save(call)
    elif call.data == 'delete':
        logger.debug('Вызываем удаление сообщения')
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            logger.info('Сообщение успешно удалено')
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {str(e)}")


bot.polling(none_stop=True)