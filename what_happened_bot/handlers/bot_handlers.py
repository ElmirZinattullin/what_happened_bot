from typing import Dict

from telebot import TeleBot

from telebot.types import Message, PhotoSize

from keyborads import keyboards, buttons
from states.bot_states import WhatHappenedStates
from templates.qeustions import QUESTIONS
from templates import message as msg
from settings.settings import set_support_chat_id, SUPPORT_CHAT_ID
from .handler_utils import change_state, send_users_question, send_users_feedback


def set_handlers(bot: TeleBot):
    chat_id_handlers(bot)
    support_chat_id_register_handlers(bot)
    start_handlers(bot)
    main_menu_handlers(bot)
    complaints_and_suggestions_menu_handlers(bot)
    faq_menu_handlers(bot)
    address_input_handler(bot)
    feed_back_input_handler(bot)
    send_photo_menu_handler(bot)
    send_number_menu_handler(bot)

def chat_id_handlers(bot: TeleBot):
    @bot.message_handler(commands=["chat_id"])
    def chat_id(message: Message):
        bot.send_message(message.chat.id, f"Chat_id = {message.chat.id}")

def support_chat_id_register_handlers(bot: TeleBot):
    @bot.message_handler(commands=["register_support"])
    def register_support(message: Message):
        bot.send_message(message.chat.id, f"Chat_id = {message.chat.id}")
        set_support_chat_id(str(message.chat.id))
        pass


def start_handlers(bot: TeleBot):
    @bot.message_handler(commands=["start"], chat_types=["private"])
    def start(message: Message):
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=msg.WELLCOME.format(message.from_user.first_name),
            keyboard=keyboards.MAIN_MENU
        )
        bot.reset_data(message.from_user.id)


def main_menu_handlers(bot: TeleBot):
    state = WhatHappenedStates.main_menu

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.FAQ,
        chat_types=["private"]
    )
    def go_to_faq_menu(message: Message):
        send_message = msg.FAQ
        questions_msg = ""
        for i, question in enumerate(QUESTIONS.keys()):
            numerate_question = f'{i + 1} - {question}\n'
            questions_msg += numerate_question
        send_message = "\n".join((send_message, questions_msg))
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.faq_menu,
            sending_message=send_message,
            keyboard=keyboards.FAQ
        )

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.COMPLAINTS_AND_SUGGESTIONS,
        chat_types=["private"]
    )
    def go_to_complaints_and_suggestions_menu(message: Message):
        send_message = msg.COMPLAINTS_AND_SUGGESTIONS
        bot.reset_data(message.from_user.id)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.complaints_and_suggestions_menu,
            sending_message=send_message,
            keyboard=keyboards.COMPLAINTS_AND_SUGGESTIONS
        )

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.BACK,
        chat_types=["private"]
    )
    def go_to_main_menu(message: Message):
        send_message = msg.BACK_TO_MAIN_MENU

        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=send_message,
            keyboard=keyboards.MAIN_MENU
        )


def complaints_and_suggestions_menu_handlers(bot):
    state = WhatHappenedStates.complaints_and_suggestions_menu

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.SEND_COMPLAIN or message.text == buttons.SEND_FEEDBACK,
        chat_types=["private"]
    )
    def go_to_address_menu(message: Message):
        send_message = msg.CHOOSING_ADDRESS
        with bot.retrieve_data(message.from_user.id) as data:
            if message.text == buttons.SEND_COMPLAIN:
                data["feedback_type"] = "complain"
            else:
                data["feedback_type"] = "feedback"
        keyboard, is_end = keyboards.ADDRESS_KEYBOARD_OBJ.get_keyboard()
        bot.set_state(message.from_user.id, state=WhatHappenedStates.clinic_address_choosing)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.clinic_address_choosing,
            sending_message=send_message,
            keyboard=keyboard
        )


    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.BACK,
        chat_types=["private"]
    )
    def go_to_main_menu(message: Message):
        send_message = msg.BACK_TO_MAIN_MENU
        bot.reset_data(message.from_user.id)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=send_message,
            keyboard=keyboards.MAIN_MENU
        )


def faq_menu_handlers(bot):
    state = [WhatHappenedStates.faq_menu, WhatHappenedStates.new_question_input]
    support_chat_id = SUPPORT_CHAT_ID

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.BACK,
        chat_types=["private"]
    )
    def go_to_main_menu(message: Message):
        send_message = msg.BACK_TO_MAIN_MENU
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=send_message,
            keyboard=keyboards.MAIN_MENU
        )

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.ASK_YOUR_QUESTION,
        chat_types=["private"]
    )
    def go_to_ask_your_question(message: Message):
        send_message = msg.ASK_YOUR_QUESTION
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.new_question_input,
            sending_message=send_message,
        )


    @bot.message_handler(
        state=state,
        func=lambda message: message.text in keyboards.FAQ.buttons,
        chat_types=["private"]
    )
    def go_to_faq_and_get_answer(message: Message):
        send_message = "Ответа не найдено"
        for i, question in enumerate(QUESTIONS.keys()):
            if message.text == str(i + 1):
                send_message = QUESTIONS[question]
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.faq_menu,
            sending_message=send_message,
            keyboard=keyboards.FAQ
        )

    @bot.message_handler(
        state=WhatHappenedStates.new_question_input,
        chat_types=["private"]
    )
    def input_user_question(message: Message):
        send_message = msg.SEND_QUESTION_NUMBER + 2*"\n" + msg.INDIVIDUAL_DATA_NOTIFICATION
        with bot.retrieve_data(message.from_user.id) as data:
            data["user_question"] = message.text
        # send_users_question(bot, message)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.phone_number_send_menu,
            sending_message=send_message,
            keyboard=keyboards.SEND_NUMBER
        )


def address_input_handler(bot: TeleBot):
    state = WhatHappenedStates.clinic_address_choosing

    @bot.message_handler(
        state=state,
        regexp=buttons.TO_MAIN_MENU,
        chat_types=["private"]
    )
    def get_feedback(message: Message):
        bot.reset_data(message.from_user.id)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=msg.BACK_TO_MAIN_MENU,
            keyboard=keyboards.MAIN_MENU
        )

    @bot.message_handler(
        state=state,
        chat_types=["private"],
        regexp=buttons.BACK
    )
    def choosing_address_menu_back(message: Message):
        with bot.retrieve_data(message.from_user.id) as data:
            address = data.get("address")
        if address:
            address_args = address.split("%%")
        else:
            change_state(
                bot=bot,
                message=message,
                new_state=WhatHappenedStates.complaints_and_suggestions_menu,
                sending_message=msg.COMPLAINTS_AND_SUGGESTIONS,
                keyboard=keyboards.COMPLAINTS_AND_SUGGESTIONS
            )
            return
        address_args = address_args[:-1]
        keyboard, is_end = keyboards.ADDRESS_KEYBOARD_OBJ.get_keyboard(*address_args)
        address = "%%".join(address_args)
        with bot.retrieve_data(message.from_user.id) as data:
            data["address"] = address
        send_message = "Вводимый адрес:" + " > ".join(address_args)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.clinic_address_choosing,
            sending_message=send_message,
            keyboard=keyboard
        )

    @bot.message_handler(
        state=state,
        chat_types=["private"]
    )
    def choosing_address_menu(message: Message):
        with bot.retrieve_data(message.from_user.id) as data:
            address = data.get("address")
        if address:
            address_args = address.split("%%")
        else:
            address_args = []
        try:
            keyboard, is_end = keyboards.ADDRESS_KEYBOARD_OBJ.get_keyboard(*address_args)
            prev_keyboard_buttons = keyboard.buttons
        except keyboards.AddressKeyboard.AddressKeyboardKeyError:
            send_message = msg.CHOOSING_ADDRESS
            keyboard, is_end = keyboards.ADDRESS_KEYBOARD_OBJ.get_keyboard()
            bot.set_state(message.from_user.id, state=WhatHappenedStates.clinic_address_choosing)
            change_state(
                bot=bot,
                message=message,
                new_state=WhatHappenedStates.clinic_address_choosing,
                sending_message=send_message,
                keyboard=keyboard
            )
        else:
            if message.text in prev_keyboard_buttons:
                address_args.append(message.text)
                with bot.retrieve_data(message.from_user.id) as data:
                    address = "%%".join(address_args)
                    data["address"] = address
                send_message ="Вводимый адрес:" + " > ".join(address_args)
                try:
                    keyboard, is_end = keyboards.ADDRESS_KEYBOARD_OBJ.get_keyboard(*address_args)
                except keyboards.AddressKeyboard.AddressKeyboardKeyError:
                    return
                if is_end:
                    with bot.retrieve_data(message.from_user.id) as data:
                        feedback_type = data.get("feedback_type")
                    if feedback_type == "complain":
                        send_message = msg.COMPLAINT.format(clinic=keyboard)
                    else:
                        send_message = msg.FEEDBACK.format(clinic=keyboard)
                    change_state(
                        bot=bot,
                        message=message,
                        new_state=WhatHappenedStates.feedback_input,
                        sending_message=send_message,
                        keyboard=keyboards.DEFAULT
                    )
                else:
                    send_message = "Вводимый адрес:" + " > ".join(address_args)
                    change_state(
                        bot=bot,
                        message=message,
                        new_state=WhatHappenedStates.clinic_address_choosing,
                        sending_message=send_message,
                        keyboard=keyboard
                    )
            else:
                send_message = "Пожалуйста выберите из предложенных вариантов"
                change_state(
                    bot=bot,
                    message=message,
                    new_state=WhatHappenedStates.clinic_address_choosing,
                    sending_message=send_message,
                )





def feed_back_input_handler(bot:TeleBot):
    state = WhatHappenedStates.feedback_input

    @bot.message_handler(
        state=state,
        regexp=buttons.BACK,
        chat_types=["private"]
    )
    def back_to_address(message: Message):
        with bot.retrieve_data(message.from_user.id) as data:
            address = data.get("address")
        if address:
            address_args = address.split("%%")
        else:
            change_state(
                bot=bot,
                message=message,
                new_state=WhatHappenedStates.complaints_and_suggestions_menu,
                sending_message=msg.COMPLAINTS_AND_SUGGESTIONS,
                keyboard=keyboards.COMPLAINTS_AND_SUGGESTIONS
            )
            return
        address_args = address_args[:-1]
        keyboard, is_end = keyboards.ADDRESS_KEYBOARD_OBJ.get_keyboard(*address_args)
        address = "%%".join(address_args)
        with bot.retrieve_data(message.from_user.id) as data:
            data["address"] = address
        send_message = "Вводимый адрес:" + " > ".join(address_args)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.clinic_address_choosing,
            sending_message=send_message,
            keyboard=keyboard
        )

    @bot.message_handler(
        state=state,
        regexp=buttons.TO_MAIN_MENU,
        chat_types=["private"]
    )
    def get_feedback(message: Message):
        bot.reset_data(message.from_user.id)
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=msg.BACK_TO_MAIN_MENU,
            keyboard=keyboards.MAIN_MENU
        )


    @bot.message_handler(
        state=state,
        chat_types=["private"]
    )
    def get_feedback(message: Message):
        with bot.retrieve_data(message.from_user.id) as data:
            data["feedback"] = message.text
        send_message = msg.SEND_PHOTO
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.picture_add_menu,
            sending_message=send_message,
            keyboard=keyboards.SEND_PHOTO
        )


def send_photo_menu_handler(bot):
    state = WhatHappenedStates.picture_add_menu

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.NO,
        chat_types=["private"]
    )
    def send_feedback(message: Message):
        send_message = msg.SEND_NUMBER + 2*"\n" + msg.INDIVIDUAL_DATA_NOTIFICATION
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.phone_number_send_menu,
            sending_message=send_message,
            keyboard=keyboards.SEND_NUMBER
        )

    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.YES,
        chat_types=["private"]
    )
    def go_to_send_photo(message: Message):
        with bot.retrieve_data(message.from_user.id) as data:
            data["photo"] = 1


    @bot.message_handler(
        state=state,
        content_types=['photo'],
        chat_types=["private"]
    )
    def send_photo(message: Message):
        with bot.retrieve_data(message.from_user.id) as data:
            is_photo_allowed = data.get("photo") == 1
        if not is_photo_allowed:
            return
        send_message = msg.SEND_NUMBER
        photo: PhotoSize = message.photo[0]
        photo_id = photo.file_id
        with bot.retrieve_data(message.from_user.id) as data:
            photo_ids = data.get("photo_ids")
            if photo_ids:
                data["photo_ids"] += [photo_id]
            else:
                data["photo_ids"] = [photo_id]
        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.phone_number_send_menu,
            sending_message=send_message,
            keyboard=keyboards.SEND_NUMBER
        )


def send_number_menu_handler(bot):
    state = WhatHappenedStates.phone_number_send_menu

    def get_params(message: Message) -> Dict[str, str]:
        params = {}
        with bot.retrieve_data(message.from_user.id) as data:
            params["is_photo_allowed"] = data.get("photo") == 1
            params["photo_ids"] = data.get("photo_ids")
            params["feedback_type"] = data.get("feedback_type")
            params["address"] = data.get("address")
            params["feedback"] = data.get("feedback")
        return params


    @bot.message_handler(
        state=state,
        func=lambda message: message.text == buttons.MAIN_MENU,
        chat_types=["private"]
    )
    def go_to_main_menu(message: Message):
        """
        Возврат в меню без отправки сообщения в тех.поддержку
        """
        send_message = msg.BACK_TO_MAIN_MENU

        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=send_message,
            keyboard=keyboards.MAIN_MENU
        )


    @bot.message_handler(
        state=state,
        content_types=['contact']
    )
    def go_to_phone_number_request(message: Message):

        contact = message.contact
        send_message = msg.BACK_TO_MAIN_MENU

        with bot.retrieve_data(message.from_user.id) as data:
            question = data.get("user_question")

        if question is not None:
            send_users_question(bot, question, contact)
        else:
            params = get_params(message)
            send_users_feedback(bot, params, contact)

        change_state(
            bot=bot,
            message=message,
            new_state=WhatHappenedStates.main_menu,
            sending_message=send_message,
            keyboard=keyboards.MAIN_MENU
        )



# def send_number_request_handler(bot):
#     state = WhatHappenedStates.phone_number_send_request
#
#     @bot.message_handler(
#         state=state,
#         chat_types=["private"]
#     )
#     def go_to_main_menu(message: Message):
#         send_message = msg.BACK_TO_MAIN_MENU
#
#         send_users_feedback(bot, message, feedback_type="Жалоба")
#
#         change_state(
#             bot=bot,
#             message=message,
#             new_state=WhatHappenedStates.main_menu,
#             sending_message=send_message,
#             keyboard=keyboards.MAIN_MENU
#         )
