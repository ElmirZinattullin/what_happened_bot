from typing import Optional, List

from telebot import State, TeleBot
from telebot.types import ReplyKeyboardMarkup, Message, Contact

from templates.suuport_chat_message import QUESTION, FEEDBACK


def change_state(bot, message: Message, new_state:State, sending_message:str, keyboard:Optional[ReplyKeyboardMarkup]=None):
    bot.send_message(message.chat.id, sending_message, reply_markup=keyboard)
    bot.set_state(message.from_user.id, state=new_state)


def send_users_question(bot: TeleBot, question_text, contact:Optional[Contact] = None):
    from settings.settings import SUPPORT_CHAT_ID
    if not SUPPORT_CHAT_ID:
        return
    support_chat_id = SUPPORT_CHAT_ID
    bot.send_message(support_chat_id, QUESTION.format(question=question_text))
    send_contact(bot, contact, support_chat_id)


def send_users_feedback(bot: TeleBot, params:dict, contact:Optional[Contact] = None):
    from settings.settings import SUPPORT_CHAT_ID
    if not SUPPORT_CHAT_ID:
        return
    support_chat_id = SUPPORT_CHAT_ID
    feedback_type = params["feedback_type"]
    if feedback_type == "complain":
        feedback_type = "Жалоба"
    else:
        feedback_type = "Отзыв"
    feedback = FEEDBACK.format(
        feedback_type = feedback_type,
        clinic = " ".join(params["address"].split("%%")),
        is_photo_allowed = params["is_photo_allowed"],
        text = params["feedback"]
    )
    bot.send_message(support_chat_id, feedback)
    send_contact(bot, contact, support_chat_id)
    if params.get("photo_ids"):
        send_photo_by_id(bot, params.get("photo_ids"), support_chat_id)

def send_photo_by_id(bot: TeleBot, photo_ids:List[str], support_chat_id:int):
    for photo_id in photo_ids:
        bot.send_photo(support_chat_id, photo_id, caption="Фото к отзыву")

def send_contact(bot: TeleBot, contact:Optional[Contact], support_chat_id:int):
    if contact:
        bot.send_contact(
            support_chat_id,
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name,
            vcard=contact.vcard
        )