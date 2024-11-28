from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown
import requests

from utils import logger, Endpoints, get_surveillance_from_list_by_name, get_surveillance_from_list_by_enumerate_index, get_pretty_enumerate_list_of_surveillances
from routers.keyboards import ActionsButtonText
from .states import Surveillance

router = Router(name=__name__)

@router.message(F.text == ActionsButtonText.CreateSurveillance)
async def handle_create_surveillance(msg: Message, state: FSMContext):
    await state.set_state(Surveillance.name)
    text = markdown.text(
        "Введите псевдоним объекта",
        sep="\n"
    )
    await msg.answer(text=text)

@router.message(Surveillance.name, F.text)
async def handle_surveillance_name(msg: Message, state: FSMContext):
    await state.clear()

    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    new_surveillance = {
        "name":msg.text,
        "user_id": user["id"],
    }
    response = requests.post(Endpoints.PostSurveillance, json=new_surveillance)
    logger.info(response.status_code)
    if response.status_code == 200:
        await msg.answer(
            f"Поздравляю, вы добавили объект {markdown.hbold(new_surveillance["name"])}!",
        )
    elif response.status_code == 409:
        await msg.answer(
            f"У вас уже имеется данная тема {markdown.hbold(new_surveillance["name"])}"
        )
    else:
        await msg.answer(
            f"Извините, что-то пошло не так... 😢"
        )

@router.message(Surveillance.name)
async def handle_invalid_surveillance_name(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        f"Извините, я понимаю только текстовые названия тем."
    )

@router.message(F.text == ActionsButtonText.ShowSurveillance)
async def handle_show_surveillances(msg: Message):
    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    params = {
        "user_id": user["id"]
    }
    user_surveillances = requests.get(Endpoints.ShowUserSurveillances, params=params).json()

    if user_surveillances:
        text = get_pretty_enumerate_list_of_surveillances(user_surveillances)
        await msg.answer(f"{text}")
    else:
        await msg.answer(f"Вы ещё не добавили ни одного объекта")

@router.message(F.text == ActionsButtonText.DeleteSurveillance)
async def handle_delete_theme(msg: Message, state: FSMContext):
    await state.set_state(Surveillance.delete)
    await msg.answer(f"Введите псевдоним объекта или его порядковый номер")

@router.message(Surveillance.delete, F.text)
async def handle_delete_theme_name(msg: Message, state: FSMContext):
    await state.clear()

    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    params = {
        "user_id": user["id"]
    }
    user_themes = requests.get(Endpoints.ShowUserSurveillances, params=params).json()


    search_surveillance_by_name = get_surveillance_from_list_by_name(user_themes, msg.text)
    search_surveillance_by_number = get_surveillance_from_list_by_enumerate_index(user_themes, msg.text)
    logger.info(f"search_surveillance_by_number = {search_surveillance_by_number}")

    search_surveillance = None
    if search_surveillance_by_name:
        search_surveillance = search_surveillance_by_name
    elif search_surveillance_by_number:
        search_surveillance = search_surveillance_by_number
    else:
        await msg.answer(text=f"Перепроверьте введеные данные, у нас не получилось найти такого объекта")

    if search_surveillance:
        response = requests.delete(Endpoints.DeleteSurveillance, params={"surveillance_id": search_surveillance["id"]})
        if response.status_code == 200:
            await msg.answer(
                text=f"Успешно удален объект {search_surveillance['name']}!",
            )
        else:
            await msg.answer(
                text=f"Не удалось удалить объект"
        )