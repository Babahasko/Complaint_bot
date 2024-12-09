from typing import Union

import requests
from .endpoints import Endpoints
from aiogram.types import Message, CallbackQuery


async def request_user(input_type: Union[Message, CallbackQuery]):
    params = {
        "telegramm_account": input_type.from_user.username,
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
    user = await request_user(callback)

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

async def request_user_complains(input_type: Union[Message, CallbackQuery]):
    user = await request_user(input_type)
    params = {
        "user_id": user["id"]
    }
    user_complains = requests.get(Endpoints.ShowUserComplains, params=params).json()
    return user_complains


