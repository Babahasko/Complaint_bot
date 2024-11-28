from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown
import requests

from utils import logger, Endpoints, get_theme_from_list_by_name, get_theme_from_list_by_enumerate_index, get_pretty_enumerate_list_of_themes
from routers.keyboards import ActionsButtonText
from .states import Theme

router = Router(name=__name__)

@router.message(F.text == ActionsButtonText.CreateTheme)
async def handle_create_theme(msg: Message, state: FSMContext):
    await state.set_state(Theme.name)
    text = markdown.text(
        "Введите название темы",
        sep="\n"
    )
    await msg.answer(text=text)

@router.message(Theme.name, F.text)
async def handle_theme_name(msg: Message, state: FSMContext):
    await state.clear()

    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    new_theme = {
        "name":msg.text,
        "user_id": user["id"],
    }
    response = requests.post(Endpoints.PostTheme, json=new_theme)
    logger.info(response.status_code)
    if response.status_code == 200:
        await msg.answer(
            f"Поздравляю, вы добавили тему {markdown.hbold(new_theme["name"])}!",
        )
    elif response.status_code == 409:
        await msg.answer(
            f"У вас уже имеется данная тема {markdown.hbold(new_theme["name"])}"
        )
    else:
        await msg.answer(
            f"Извините, что-то пошло не так... 😢"
        )

@router.message(Theme.name)
async def handle_invalid_theme_name(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        f"Извините, я понимаю только текстовые названия тем."
    )

@router.message(F.text == ActionsButtonText.ShowTheme)
async def handle_show_theme(msg: Message):
    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    params = {
        "user_id": user["id"]
    }
    user_themes = requests.get(Endpoints.ShowUserThemes, params=params).json()
    if user_themes:
        text = get_pretty_enumerate_list_of_themes(user_themes)
        await msg.answer(f"{text}")
    else:
        await msg.answer(f"Вы ещё не добавили ни одной темы")

@router.message(F.text == ActionsButtonText.DeleteTheme)
async def handle_delete_theme(msg: Message, state: FSMContext):
    await state.set_state(Theme.delete)
    await msg.answer(f"Введите название темы или её порядковый номер")

@router.message(Theme.delete, F.text)
async def handle_delete_theme_name(msg: Message, state: FSMContext):
    await state.clear()

    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    params = {
        "user_id": user["id"]
    }
    user_themes = requests.get(Endpoints.ShowUserThemes, params=params).json()


    search_theme_by_name = get_theme_from_list_by_name(user_themes, msg.text)
    search_theme_by_number = get_theme_from_list_by_enumerate_index(user_themes, msg.text)
    logger.info(f"search_theme_by_number = {search_theme_by_number}")

    search_theme = None
    if search_theme_by_name:
        search_theme = search_theme_by_name
    elif search_theme_by_number:
        search_theme = search_theme_by_number
    else:
        await msg.answer(text=f"Перепроверьте введеные данные, у нас не получилось найти такой темы")

    if search_theme:
        response = requests.delete(Endpoints.DeleteTheme, params={"theme_id": search_theme["id"]})
        if response.status_code == 200:
            await msg.answer(
                text=f"Успешно удалена тема {search_theme['name']}!",
            )
        else:
            await msg.answer(
                text=f"Не удалось удалить тему"
        )