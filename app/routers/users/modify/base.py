from aiogram.fsm.state import State, StatesGroup


class UserModifyForm(StatesGroup):
    ADMIN = State()
    CONFIRM = State()
    INPUT = State()
    CONFIGS = State()
