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

from utils import (request_user,
                   request_user_themes,
                   request_user_surveillances,
                   request_create_complain,
                   request_user_complains,
                   request_delete_complain)

from routers.keyboards import (get_inline_themes_keyboard,
                               get_inline_surveillance_keyboard,
                               get_confirming_keyboard)
from utils.help_complain_handler_functions import (get_pretty_enumerate_list_of_complains,
                                                   get_complain_from_list_by_enumerate_index)
from .states import Complain

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

@router.callback_query(ComplaintForm.confirming, F.data.startswith("complain_"))
async def handle_confirming_complain(callback: CallbackQuery, state: FSMContext):
    choosen_button = callback.data.split("_")[1]
    match choosen_button:
        case "confirm":
            state_data = await state.get_data()

            surveillance_name = state_data["choosen_surveillance"]
            theme_name = state_data["choosen_theme"]
            surveillance_id = state_data["choosen_surveillance_id"]
            theme_id = state_data["choosen_theme_id"]
            response = await request_create_complain(callback, surveillance_id, theme_id)

            if response.status_code == 200:
                await callback.message.edit_text(f"Запись 'Объект: {surveillance_name},"
                                                 f" Тема жалобы: {theme_name}' занесена в базу данных")
            else:
                await callback.message.edit_text(
                    f"Извините, что-то пошло не так... 😢"
                )
        case "decline":
            await callback.message.edit_text(f"Внесение жалобы отменено")
    await state.clear()

@router.message(F.text == ActionsButtonText.ShowComplain)
async def handle_show_complain(msg: Message):
    user_complains = await request_user_complains(msg)
    logger.info(f"user_complains {user_complains}")

    if user_complains:
        text = get_pretty_enumerate_list_of_complains(user_complains)
        await msg.answer(f"{text}")
    else:
        await msg.answer(f"Вы ещё не добавили ни одного объекта")

@router.message(F.text == ActionsButtonText.DeleteComplain)
async def handle_delete_theme(msg: Message, state: FSMContext):
    await state.set_state(Complain.delete)
    await msg.answer(f"Введите порядковый номер записи")

@router.message(Complain.delete, F.text)
async def handel_delete_complain(msg: Message, state: FSMContext):
    await state.clear()
    user_complains = await request_user_complains(msg)
    search_complain = get_complain_from_list_by_enumerate_index(user_complains, msg.text)
    if search_complain is None:
        await msg.answer(text=f"Перепроверьте введенные данные,"
                              f" указанная запись не была найдена")
    else:
        response = await request_delete_complain(search_complain['id'])
        if response.status_code == 200:
            theme = search_complain['theme']
            surveillance = search_complain['surveillance']
            data = search_complain['readable_data']
            await msg.answer(
                text=f"Успешно удалена запись: {surveillance} {theme} {data}!",
            )
        else:
            await msg.answer(
                text=f"Не удалось удалить объект"
        )

