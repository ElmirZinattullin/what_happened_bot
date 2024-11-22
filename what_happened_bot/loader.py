import logging

from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from middlewares.middleware import LogMessageMiddleware

def get_bot():
    storage = StateMemoryStorage()
    print(config.BOT_TOKEN)
    bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage, use_class_middlewares=True)
    bot.setup_middleware(LogMessageMiddleware())
    return bot

def set_logger():
    level = config.LOG_LEVEL.upper()
    if level:
        try:
            # print(level)
            logging.basicConfig(level=level)
        except ValueError:
            logging.error("Invalid LOGGER_LEVEL. Choose: CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG")

