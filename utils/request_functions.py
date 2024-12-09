import requests
from .endpoints import Endpoints
from aiogram.types import Message, CallbackQuery


async def request_user(msg: Message):
    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()
    return user

async def request_user_themes(msg: Message):
    params = {
        "telegramm_account": msg.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    params = {
        "user_id": user["id"]
    }
    user_themes = requests.get(Endpoints.ShowUserThemes, params=params).json()
    return user_themes

async def request_user_surveillances(callback: CallbackQuery):
    params = {
        "telegramm_account": callback.from_user.username,
    }
    user = requests.get(Endpoints.GetUser, params=params).json()

    params = {
        "user_id": user["id"]
    }
    user_surveillances = requests.get(Endpoints.ShowUserSurveillances, params=params).json()
    return user_surveillances