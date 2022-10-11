from aiogram.dispatcher.filters.state import State, StatesGroup

class Groups(StatesGroup):
    groups = State()
    country = State()