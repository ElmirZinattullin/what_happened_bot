from typing import Dict, Union

from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import telebot

class Keyboard(ReplyKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

def main_menu_keyboard() -> Keyboard:
    """Кнопки в главном меню"""
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    buttons = "Часто задаваемы вопросы", "Жалобы и предложения"
    keyboard.add(*buttons)
    return keyboard


def complaints_and_suggestions_menu_keyboard() -> Keyboard:
    """ Кнопки в меню жалобы и предложения"""
    keyboard = Keyboard(row_width=1, resize_keyboard=True)
    buttons = "Часто задаваемы вопросы", "Жалобы и предложения", "Назад"
    keyboard.add(*buttons)
    return keyboard

# Map = Union[Dict[str, str], Dict[str, "Map"]]

class AddressKeyboard:

    class AddressKeyboardException(Exception):
        pass

    def __init__(self, one_map: dict):
        self.map = one_map


    @staticmethod
    def get_in_deep(one_map, *args):
        if not isinstance(one_map, dict):
            raise AddressKeyboard.AddressKeyboardException(f"Couldn't get key='{args[0]}' on {one_map}")
        result = one_map.get(args[0])
        if len(args) > 1 and result:
            return AddressKeyboard.get_in_deep(result, *args[1:])
        else:
            if isinstance(result, dict):
                return list(result.keys())
            else:
                return result

    def get_keyboard(self, *args):
        default_buttons = ["Назад", "К главному меню"]
        buttons = self.get_in_deep(self.map, *args)
        if buttons:
            buttons += default_buttons
        else:
            buttons = default_buttons
        keyboard = Keyboard(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        return keyboard




if __name__ == '__main__':
    addres = {
        "Tatarstan": {
            "Kazan": {
                "Svoboda": ["sv_perv_bolnica", "sv_vtoraya_bolnica"],
                "Kremlevsaya": ["kreml 1", "kreml 2"],
            },
            "Elabuga": {
                "Prolet": ["elbuj perv bolnica"]
            }
        }
    }
    res = AddressKeyboard(one_map=addres).get_keyboard("Tatarstan", "Kazan", "Svoboda", "sv_perv_bolnica").buttons
    print(res)