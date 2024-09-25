from loader import get_bot
from handlers.bot_hanlers import set_handlers
from telebot.custom_filters import StateFilter
from telebot import TeleBot

if __name__ == "__main__":
    bot: TeleBot = get_bot()
    bot.add_custom_filter(StateFilter(bot))
    set_handlers(bot)
    bot.infinity_polling()
