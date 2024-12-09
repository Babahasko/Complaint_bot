from random import randint
from typing import Optional, List

from aiogram import Router
from aiogram.filters import Command
from aiogram import F
from routers.keyboards import ActionsButtonText
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from utils import logger

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from utils import request_user_themes, request_user_surveillances
from routers.keyboards import get_inline_themes_keyboard, get_inline_surveillance_keyboard, get_confirming_keyboard

router = Router(name=__name__)

class ComplaintForm(StatesGroup):
    choosing_theme = State()
    choosing_surveillance = State()
    confirming = State()

async def update_message_for_choosing_surveillance(msg: Message, user_surveillances: List):
    surveillance_keyboard = get_inline_surveillance_keyboard(user_surveillances)
    await msg.edit_text(
        f"Теперь выберете объект",
        reply_markup=surveillance_keyboard
    )

async def update_message_for_confirm_surveillance(msg: Message, surveillance_name, theme_name):
    confirming_keyboard = get_confirming_keyboard()
    await msg.edit_text(
        f"Подтвердите запись жалобы:\n"
        f"Объект: {surveillance_name}, Тема жалобы: {theme_name}",
        reply_markup=confirming_keyboard
    )

@router.message(F.text == ActionsButtonText.CreateComplain)
async def handle_start_complain(msg: Message, state: FSMContext):
    await state.set_state(ComplaintForm.choosing_theme)
    user_themes = await request_user_themes(msg)
    theme_keyboard = get_inline_themes_keyboard(user_themes)
    await msg.answer("Выберите тему:", reply_markup=theme_keyboard)

@router.callback_query(ComplaintForm.choosing_theme, F.data.startswith("theme_"))
async def handle_choosing_theme(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    theme_name = callback.data.split("_")[1]
    theme_id = callback.data.split("_")[2]
    await state.update_data(choosen_theme=theme_name)
    await state.update_data(choosen_theme_id=theme_id)

    state_data = await state.get_data()
    logger.info(f"state_data = {state_data}")

    await callback.answer(f"Вы выбрали тему: {theme_name}")
    user_surveillances = await request_user_surveillances(callback)
    await update_message_for_choosing_surveillance(callback.message, user_surveillances)

    await state.set_state(ComplaintForm.choosing_surveillance)

@router.callback_query(ComplaintForm.choosing_surveillance, F.data.startswith("surveillance_"))
async def handle_choosing_surveillance(callback: CallbackQuery, state: FSMContext):
    # await state.clear()

    surveillance_name = callback.data.split("_")[1]
    surveillance_id = callback.data.split("_")[2]
    await state.update_data(choosen_surveillance=surveillance_name)
    await state.update_data(choosen_surveillance_id=surveillance_id)

    await callback.answer(f"Вы выбрали объект: {surveillance_name}")

    state_data = await state.get_data()
    logger.info(f"state_data = {state_data}")

    surveillance_name = state_data["choosen_surveillance"]
    theme_name = state_data["choosen_theme"]
    await update_message_for_confirm_surveillance(callback.message, surveillance_name, theme_name)

    await state.set_state(ComplaintForm.confirming)

