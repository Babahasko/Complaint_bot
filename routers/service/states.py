from aiogram.fsm.state import StatesGroup, State

class Theme(StatesGroup):
    name = State()
    delete = State()

class Surveillance(StatesGroup):
    name = State()
    delete = State()