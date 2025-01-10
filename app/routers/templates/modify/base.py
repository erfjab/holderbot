from aiogram.fsm.state import State, StatesGroup


class TemplateModifyForm(StatesGroup):
    CONFIRM = State()
    DATA_LIMIT = State()
    DATE_TYPE = State()
    DATE_LIMIT = State()
    INPUT = State()
