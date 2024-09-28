from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config

def get_bot():
    storage = StateMemoryStorage()
    print(config.BOT_TOKEN)
    return TeleBot(token=config.BOT_TOKEN, state_storage=storage)