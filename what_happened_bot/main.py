import sys
import os
sys.path.insert(0, os.path.relpath("."))

from loader import get_bot
from handlers.bot_handlers import set_handlers
from telebot.custom_filters import StateFilter
from telebot import TeleBot
from templates.description import DESCRIPTION, LANGUAGE

if __name__ == "__main__":
    bot: TeleBot = get_bot()
    bot.set_my_description(DESCRIPTION, LANGUAGE)
    bot.add_custom_filter(StateFilter(bot))
    set_handlers(bot)
    bot.infinity_polling()