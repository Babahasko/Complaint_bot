from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class RegisterButtonText:
    REGISTER = "Зарегистрироваться"
    STOP = "Остановить регистрацию"

def get_register_keyboard():
    button_register = KeyboardButton(text=RegisterButtonText.REGISTER)

    buttons_row = [button_register]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_row],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup

def get_stop_keyboard():
    button_stop = KeyboardButton(text=ButtonText.STOP)
    button_row = [button_stop]
    markup = ReplyKeyboardMarkup(
        keyboard=[button_row],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup

#
# def get_on_start_keyboard():
#     button_hello = KeyboardButton(text=ButtonText.HELLO)
#     button_bye = KeyboardButton(text=ButtonText.BYE)
#     buttons_row_1 = [button_hello]
#     buttons_row_2 = [button_bye]
#     markup = ReplyKeyboardMarkup(
#         keyboard=[buttons_row_1, buttons_row_2],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#     )
#     return markup



# builder = ReplyKeyboardBuilder()
# numbers = ["🔍","😌","3","4","5","1","2","3","4","5","1","2","3","4","5"]
# for key in numbers:
#     builder.button(text=key)
#     builder.adjust(1)
# return builder.as_markup(resize_keyboard=True)
