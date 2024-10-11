from aiogram.fsm.state import StatesGroup, State


class UserCreateForm(StatesGroup):
    base_username = State()
    start_number = State()
    how_much = State()
    data_limit = State()
    date_limit = State()
    status = State()
    admin = State()
    inbounds = State()
