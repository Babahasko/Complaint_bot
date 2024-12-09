from typing import Union

import requests
from .endpoints import Endpoints
from aiogram.types import Message, CallbackQuery


async def request_user(input: Union[Message, CallbackQuery]):
    params = {
        "telegramm_account": input.from_user.username,
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

async def request_create_complain(callback: CallbackQuery, surveillance_id, theme_id):
    user = await request_user(callback)
    new_complain = {
        "user_id": user["id"],
        "surveillance_id": surveillance_id,
        "theme_id": theme_id
    }
    response = requests.post(Endpoints.PostComplain, json=new_complain)
    return response
