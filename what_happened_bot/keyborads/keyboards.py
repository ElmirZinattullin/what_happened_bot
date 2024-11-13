from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from . import buttons as btn
from templates.qeustions import QUESTIONS
from templates.address import ADDRESS

class Keyboard(ReplyKeyboardMarkup):
    def __init__(self, *args, one_time_keyboard=True, **kwargs):
        super().__init__(*args, one_time_keyboard=one_time_keyboard, **kwargs)
        self.buttons = []

    def add(self, *args, row_width=None) -> 'ReplyKeyboardMarkup':
        result = super().add(*args, row_width=None)
        self.buttons += list(args)
        return result

    def row(self, *args) -> 'ReplyKeyboardMarkup':
        result = super().row(*args)
        self.buttons += list(args)
        return result

    def get_buttons(self):
        return self.buttons


def add_back_button(keyboard: Keyboard):
    """Добавление кнопки 'назад' """
    back_button = btn.BACK
    keyboard.add(back_button, row_width=1)

def add_return_to_main_button(keyboard: Keyboard):
    """Добавление кнопки 'К главному меню' """
    return_button = btn.TO_MAIN_MENU
    keyboard.add(return_button, row_width=1)

def add_main_button(keyboard: Keyboard):
    """Добавление кнопки 'Главное меню' """
    button = btn.MAIN_MENU
    keyboard.add(button, row_width=1)

def default_keyboard():
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    add_back_button(keyboard)
    add_return_to_main_button(keyboard)
    return keyboard

def main_menu_keyboard() -> Keyboard:
    """Кнопки в главном меню"""
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    buttons = btn.FAQ, btn.COMPLAINTS_AND_SUGGESTIONS
    keyboard.add(*buttons)
    return keyboard


def complaints_and_suggestions_menu_keyboard() -> Keyboard:
    """ Кнопки в меню жалобы и предложения"""
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    buttons = btn.SEND_FEEDBACK, btn.SEND_COMPLAIN
    keyboard.add(*buttons)
    add_back_button(keyboard)
    return keyboard


def faq_keyboard(faq_dict: dict, rows_width: int) -> Keyboard:
    keyboard = Keyboard(row_width=rows_width, resize_keyboard=True)
    faq_len = len(faq_dict)
    rows_amount = faq_len // rows_width + 1
    buttons = []
    for i in range(1, 1 + rows_amount * rows_width):
        if i <= faq_len:
            buttons.append(str(i))
        else:
            buttons.append(btn.NULL)
    keyboard.add(*buttons, row_width=rows_width)
    keyboard.add(btn.ASK_YOUR_QUESTION, row_width=1)
    add_back_button(keyboard)
    return keyboard


def yes_or_no_keyboard() -> Keyboard:
    """ меню Да/Нет"""
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    buttons = btn.YES, btn.NO
    keyboard.add(*buttons)
    return keyboard


def send_number_keyboard() -> Keyboard:
    """ меню для отправки номера """
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    button = KeyboardButton(btn.SEND_PHONE_NUMBER, request_contact=True)
    keyboard.add(button)
    add_main_button(keyboard)
    return keyboard


class AddressKeyboard:

    address_row = 2

    class AddressKeyboardException(Exception):
        pass

    class AddressKeyboardKeyError(Exception):
        pass

    def __init__(self, one_map: dict):
        self.map = one_map


    @staticmethod
    def get_in_deep(one_map, *args):
        if not isinstance(one_map, dict):
            raise AddressKeyboard.AddressKeyboardException(f"Couldn't get key='{args[0]}' on {one_map}")
        result = one_map
        if args:
            result = one_map.get(args[0])
        if len(args) > 1 and result:
            return AddressKeyboard.get_in_deep(result, *args[1:])
        else:
            if result is None:
                raise AddressKeyboard.AddressKeyboardKeyError(f"Couldn't get key='{args[0]}' on {one_map.keys()}")
            if isinstance(result, dict):
                address_level = AddressKeyboard.check_in_deep(result)
                if isinstance(address_level, dict):
                    return list(address_level.keys())
                else:
                    return address_level
            else:
                return result

    def get_keyboard(self, *args):
        is_end = False
        default_buttons = [btn.BACK, btn.TO_MAIN_MENU]
        keyboard = Keyboard(resize_keyboard=True, row_width=self.address_row)

        addresses = self.get_in_deep(self.map, *args)
        buttons = []
        if isinstance(addresses, str):
            is_end = True
            return addresses, is_end
        else:
            buttons += addresses
            complement = self.address_row - len(buttons) % self.address_row if len(buttons) % self.address_row else 0
            for _ in range(complement):
                buttons.append(btn.NULL)
            keyboard.add(*buttons, row_width=2)
            for button in default_buttons:
                keyboard.add(button, row_width=1)
            return keyboard, is_end


    @staticmethod
    def check_in_deep(address_dict: dict):
        """Просматривает словарь в глубину возвращает название клиники если нет других вариантов по текущему адресу или возвращает словарь с адресами на уровне выбора"""
        if len(address_dict) == 1:
            next_address = next(iter(address_dict.values()))
            if isinstance(next_address, dict):
                return AddressKeyboard.check_in_deep(next_address)
            else:
                return next_address
        else:
            return address_dict



FAQ_ROWS = 5
FAQ = faq_keyboard(QUESTIONS, rows_width=FAQ_ROWS)
MAIN_MENU = main_menu_keyboard()
COMPLAINTS_AND_SUGGESTIONS = complaints_and_suggestions_menu_keyboard()
ADDRESS_KEYBOARD_OBJ = AddressKeyboard(ADDRESS)
DEFAULT = default_keyboard()
SEND_PHOTO = yes_or_no_keyboard()
SEND_NUMBER = send_number_keyboard()

# if __name__ == '__main__':
#     addres = {
#         "Tatarstan": {
#             "Kazan": {
#                 "Svoboda": ["sv_perv_bolnica", "sv_vtoraya_bolnica"],
#                 "Kremlevsaya": ["kreml 1", "kreml 2"],
#             },
#             "Elabuga": {
#                 "Prolet": ["elbuj perv bolnica"]
#             }
#         }
#     }
#     res, is_end = AddressKeyboard(one_map=addres).get_keyboard("Tatarstan", "Kazan", "Svoboda", "sv_perv_bolnica").buttons
#     print(res)