from telebot import TeleBot
from telebot.types import Message
from keyborads import keyboards

def set_handlers(bot: TeleBot):

    @bot.message_handler()
    def echo(message: Message):
        bot.send_message(message.chat.id, message.text, reply_markup=keyboards.main_menu_keyboard())