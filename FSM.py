from aiogram.dispatcher.filters.state import State, StatesGroup

class Groups(StatesGroup):
    groups_list = State()
    channel_id = State()

class SetKeywords(StatesGroup):
    current_message = State()
    preset_name = State()

class DeleteKeywords(StatesGroup):
    preset_name = State()


class ParsingSettings(StatesGroup):
    preset_name = State()
