from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from utils import logger

class ConfirmingButtonText:
    Confirm = "Подтверждаю"
    Decline = "Отмена"

def get_inline_themes_keyboard(user_themes):
    builder = InlineKeyboardBuilder()
    for theme in user_themes:
        logger.info(f"{theme}")
        builder.button(text=f"{theme["name"]}", callback_data=f"theme_{theme["name"]}_{theme["id"]}")
        builder.adjust(4)
    return builder.as_markup()

def get_inline_surveillance_keyboard(user_surveillances):
    builder = InlineKeyboardBuilder()
    for surveillance in user_surveillances:
        builder.button(text=f"{surveillance["name"]}", callback_data=f"surveillance_{surveillance["name"]}_{surveillance["id"]}")
        builder.adjust(4)
    return builder.as_markup()

def get_confirming_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=ConfirmingButtonText.Confirm, callback_data=f"complain_confirm"))
    builder.add(InlineKeyboardButton(text=ConfirmingButtonText.Decline, callback_data=f"complain_decline"))
    return builder.as_markup()