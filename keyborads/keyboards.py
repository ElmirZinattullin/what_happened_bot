from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import telebot


# def main_menu_keyboard() -> ReplyKeyboardMarkup:
#     keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     buttons = "Часто задаваемы вопросы", "Жалобы и предложения"
#     return keyboard.add(*buttons)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, input_field_placeholder="hello")
    buttons = (str(f"{i}") for i in range(1, 31))
    keyboard.add(*buttons)
    buttons = ("A", "B")
    keyboard.add(*buttons, row_width=2)

    buttons = ("A", "B", "C", "D")
    keyboard.add(*buttons, row_width=4)
    return keyboard





def get_clother_keyboard(client_id: int) -> InlineKeyboardMarkup:
    keyboard_dict = {
        'Я отдал одежду': {'callback_data': client_id},
        'Отменить и выйти': {'callback_data': 'abort'},
    }
    return telebot.util.quick_markup(keyboard_dict, row_width=1)


"""
class telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=None, one_time_keyboard=None, 
selective=None, input_field_placeholder=None, is_persistent=None, *, api_kwargs=None)
"""

"""
class telegram.KeyboardButton(text, request_contact=None, request_location=None, request_poll=None, 
web_app=None, request_chat=None, request_users=None, *, api_kwargs=None)
"""