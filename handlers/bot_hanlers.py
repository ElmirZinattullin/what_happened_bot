from telebot import TeleBot
from telebot.types import Message
from keyborads import keyboards
from states.bot_states import WhatHappenedStates
from templates.qeustions import QUESTIONS

def set_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def start(message: Message):
        bot.send_message(message.chat.id, f"Welcome {message.from_user.username}", reply_markup=keyboards.main_menu_keyboard())
        bot.set_state(message.from_user.id, state=WhatHappenedStates.main_menu)

    @bot.message_handler(
        state=WhatHappenedStates.main_menu,
        func=lambda message: message.text == keyboards.main_menu_keyboard().buttons[0]
    )
    def main_menu_button_0(message: Message):
        answer = "Выберите номер вопроса:"
        for i, question in enumerate(QUESTIONS.keys()):
            numerate = ". ".join((str(i + 1), question))
            "\n".join((answer, numerate))
            answer = numerate
        bot.send_message(message.chat.id, answer)
        bot.set_state(message.from_user.id, state=WhatHappenedStates.faq_menu)

