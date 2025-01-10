from aiogram.fsm.state import State, StatesGroup


class UserModifyForm(StatesGroup):
    ADMIN = State()
    CONFIRM = State()
    DATA_LIMIT = State()
    DATE_LIMIT = State()
    DATE_TYPE = State()
    CONFIGS = State()
    NOTE = State()
    CHARGE = State()
    TEMPLATE = State()
