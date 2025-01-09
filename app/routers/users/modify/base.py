from aiogram.fsm.state import State, StatesGroup


class UserModifyForm(StatesGroup):
    ADMIN = State()
    CONFIRM = State()
    DATA_LIMIT = State()
    CONFIGS = State()
