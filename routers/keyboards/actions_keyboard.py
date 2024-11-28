from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class ActionsButtonText:
    CreateTheme = "Добавить тему 🌝️"
    ShowTheme = "Показать темы 🌝"
    DeleteTheme = "Удалить тему 🌝"
    CreateSurveillance = "Добавить объект 🤡"
    ShowSurveillance = "Показать объекты 🤡"
    DeleteSurveillance = "Удалить объект 🤡"
    CreateComplain = "Добавить жалобу ✍️"
    ShowComplain = "Показать жалобы ✍️"
    DeleteComplain = "Удалить жалобу ✍️"

def get_bot_actions_keyboard():
    button_create_theme = KeyboardButton(text=ActionsButtonText.CreateTheme)
    button_show_theme = KeyboardButton(text=ActionsButtonText.ShowTheme)
    button_delete_theme = KeyboardButton(text=ActionsButtonText.DeleteTheme)

    buttons_theme_row = [button_create_theme,button_show_theme, button_delete_theme]

    button_create_surveillance = KeyboardButton(text=ActionsButtonText.CreateSurveillance)
    button_show_surveillance = KeyboardButton(text=ActionsButtonText.ShowSurveillance)
    button_delete_surveillance = KeyboardButton(text=ActionsButtonText.DeleteSurveillance)

    buttons_surveillance_row = [button_create_surveillance, button_show_surveillance, button_delete_surveillance]

    button_create_complain = KeyboardButton(text=ActionsButtonText.CreateComplain)
    button_show_complain = KeyboardButton(text=ActionsButtonText.ShowComplain)
    button_delete_complain = KeyboardButton(text=ActionsButtonText.DeleteComplain)

    buttons_complain_row = [button_create_complain, button_show_complain, button_delete_complain]

    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_theme_row, buttons_surveillance_row, buttons_complain_row],
        resize_keyboard=True,
    )
    return markup
