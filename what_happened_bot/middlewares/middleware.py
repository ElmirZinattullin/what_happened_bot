import logging

import requests
import os

from telebot.handler_backends import BaseMiddleware
from telebot.types import Message
from config_data.config import LOG_API_URL, LOG_API_PASSWORD


def log_message(message: Message):
    action = None
    if message.text:
        action = message.text
    elif message.contact:
        action = f"Пользователь поделился номером телефона: {message.contact.phone_number}"
    if action and LOG_API_PASSWORD and LOG_API_URL:
        data = {
                'user_tag': message.from_user.username,
                'user_id': message.from_user.id,
                'full_name': message.from_user.full_name,
                'action': action
            }
        logging.info(data)
        data["apikey"] = LOG_API_PASSWORD
        data["bot_id"] = os.getenv("BOT_TOKEN")
        r = requests.post(LOG_API_URL, data=data, timeout=2)
        return r.status_code


class LogMessageMiddleware(BaseMiddleware):

    update_sensitive = True
    update_types = ['message', 'contact']

    def pre_process_message(self, message, data = None):
        try:
            status_code = log_message(message)
        except Exception as err:
            logging.error(f"Не смог отправить лог в админку: {err}")
            return
        if status_code and 200 <= status_code < 300:
            logging.debug("Лог отправлен успешно")
        else:
            logging.warning(f"Отправка лога провалилась код статуса не успешен: {status_code}")


    def post_process_message(self, message, data = None, exception = None):
        pass

    def pre_process_edited_message(self, message, data = None):
        pass

    def post_process_edited_message(self, message, data = None, exception = None):
        pass
