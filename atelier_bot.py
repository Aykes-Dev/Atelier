# import asyncio
import json
import logging
import requests
import sys
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

CREATE_CLAIM_URL = 'http://127.0.0.1:8000/api/create_claim'
RECIEVE_MANAGERS_URL = 'http://127.0.0.1:8000/api/managers/'
RECIEVE_BOT_TOKEN_URL = 'http://127.0.0.1:8000/api/bot/'

PHONE_NUMBER_ASK_TXT = (

    'Пожалуйста, введите номер телефона в формете +79993331122:'
)
REQUEST_MESSAGE_TXT = 'Новая заявка.\nНомер: {0}'
REQUEST_BUTTON_TEXT = 'Оставить заявку'
START_MESSAGE = ('Нажмите кнопку оставить заявку и мы '
                 'свяжемся с вами в ближайшее время.')


def logging_config():
    """Установка настроек логгирования."""
    return logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(filename=__file__ + '.log', mode='w',)
        ],
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, line:%(lineno)d, %(message)s'
    )


async def extract_phone_number(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Извлекает номер телефона из контакта."""
    phone_number = update.message.contact.phone_number
    if phone_number is not None:
        await send_request(phone_number, update, context)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=PHONE_NUMBER_ASK_TXT
        )


async def recieve_phone_number(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Извлекает номер телефона из сообщения."""
    phone_number = update.message.text
    await send_request(phone_number, update, context)


async def send_request(
    phone_number, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Посылает заявку в тг менеджера и записывает в БД."""
    data = {
        'username': update.effective_user.username,
        'phone_number': phone_number,
        'message': REQUEST_MESSAGE_TXT.format(phone_number)
    }
    response = requests.post(
        url=CREATE_CLAIM_URL,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        data=json.dumps(data)
    )
    if response.status_code == 201:
        response = requests.get(url=RECIEVE_MANAGERS_URL)
        for manager in response.json():
            if manager['to_telegram']:
                await context.bot.send_message(
                    chat_id=manager['telegram_id'],
                    text=REQUEST_MESSAGE_TXT.format(phone_number)
                )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Заявка принята'),
        )


async def start_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Отправляет сообщение с приветствием и кнопкой "Оставить заявку"."""
    keyboard = [
        [KeyboardButton(REQUEST_BUTTON_TEXT, request_contact=True)],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE,
        reply_markup=reply_markup
    )


def recieve_bot_token():
    """Получает токен бота для дальнейшей работы"""
    response = requests.get(url=RECIEVE_BOT_TOKEN_URL)
    for unit in response.json():
        if unit['active'] is True:
            return unit['token']


if __name__ == '__main__':
    logging_config()
    BOT_TOKEN = recieve_bot_token()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start_message)

    contact_handler = MessageHandler(filters.CONTACT, extract_phone_number)

    phone_number_handler = MessageHandler(
        filters.Regex(r"^\+7(\d{10})"), recieve_phone_number
    )

    application.add_handlers(
        [start_handler, phone_number_handler, contact_handler]
    )

    application.run_polling()
