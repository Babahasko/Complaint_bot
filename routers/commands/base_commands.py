import requests

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from .states import Register

from utils import logger
from routers.keyboards.base_keyboard import get_register_keyboard, get_stop_keyboard, RegisterButtonText
from routers.keyboards.actions_keyboard import  get_bot_actions_keyboard

router = Router(name=__name__)

@router.message(Command("start"))
async def start_handler(msg: Message):
    #Проверка, что юзер зарегистрирован
    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get("http://127.0.0.1:8000/user/get_user/", params=params).json()
    if user:
        await msg.answer(
            text="Начнём же работу по ведению статистики!",
            reply_markup=get_bot_actions_keyboard(),
        )
    else:
        await msg.answer(
            text=f"Пожалуйста зарегистрируйтесь!",
            reply_markup=get_register_keyboard(),
        )

@router.message(F.text == RegisterButtonText.REGISTER)
@router.message(Command("register"))
async def handle_start_register(msg: Message, state: FSMContext):
    await state.set_state(Register.username)
    await msg.answer(
        text=f"Добро пожаловать! Как мне вас звать господин {markdown.hbold(msg.from_user.username)}?",
        reply_markup=get_stop_keyboard(),
    )

@router.message(F.text == RegisterButtonText.STOP)
async def handle_stop_register(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Очень жаль, что вы не зарегистрировались... 😢")

@router.message(Register.username)
async def handle_register_username_invalid_content_type(
        msg: Message,
        state: FSMContext,
):
    await state.clear()
    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get("http://127.0.0.1:8000/user/get_user/", params=params).json()
    logger.info(user)
    if user:
        await msg.answer(f" {markdown.hbold("Вы уже зарегистрированы!")} \n"
                         f"Телеграмм аккаунт: {user["telegramm_account"]}\n "
                         f"Ник: {user["username"]}")
    else:
        await msg.answer(
        f"Извините, я понимаю только текстовые имена. Попробуйте ещё разок."
        )

@router.message(Register.username, F.text)
async def handle_register_username(msg: Message, state: FSMContext):
    await state.update_data(username=msg.text)
    await state.clear()

    new_user = {
        "telegramm_account": msg.from_user.username,
        "username": msg.text
    }
    response = requests.post("http://127.0.0.1:8000/user/register", json=new_user)
    logger.info(response.status_code)
    if response.status_code == 200:
        await msg.answer(
            f"Категорически приветствую, {markdown.hbold(msg.text)}!",
        )
    else:
        await msg.answer(
            f"Извините, что-то пошло не так... 😢"
        )


@router.message(Command("help"))
async def help_handler(msg: Message):
    text = (
        f"{markdown.hbold("Список доступных комманд")}\n"
        f"/start - Для начала использования бота достаточно нажать на меня\n"
        f"/register - Зарегистрироваться\n"
    )
    await msg.answer(
        text=text,
    )

@router.message()
async def message_handler(msg: Message):
    await msg.answer(text=f"Пагади...")
    logger.info(f"{msg.chat.id}")
    try:
        await msg.forward(chat_id=msg.chat.id)
        # await msg.copy_to(chat_id=msg.chat.id)
        # await msg.send_copy(chat_id=msg.chat.id)
    except TypeError:
        await msg.reply(text="Чо то новенькое")
# markup = get_register_keyboard()
# markup = get_on_start_keyboard()
# await msg.answer(
#     text=f"Привет {markdown.hbold(msg.from_user.username)}!"
#     f" Я помогу тебе вести статистику жалоб твоих объектов."
#     f"",
#     reply_markup=markup
# )

# @router.message(F.text == ButtonText.HELLO)

# @router.message(F.text == ButtonText.BYE)
# async def handle_bye_message(msg: Message):
#     await msg.answer(
#         text=f"See you. Click start any time!",
#         reply_markup=ReplyKeyboardRemove()
#     )

# @router.message(Command("register"))
# async def register_user(msg: Message):
#     user_id = msg.from_user.id
#     response = requests.get("http://127.0.0.1:8000/user").json()
#     logger.info(f"{response}")
#
#     all_telegramm_accounts = []
#     for user in response:
#         all_telegramm_accounts.append(user["telegramm_account"])
#
#     if user_id not in all_telegramm_accounts:
#         await msg.answer(f"Как мне вас звать господин?")
#     else:
#         await msg.answer(f"Вы уже зарегистрированы!")

# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")
#     print(msg.text)