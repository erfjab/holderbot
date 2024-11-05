"""
Module defining the states for the user creation process.
"""

from aiogram.fsm.state import StatesGroup, State


# pylint: disable=R0903
class UserCreateForm(StatesGroup):
    """
    States group for the user creation process in the bot.
    This defines the various states a user can go through while
    filling out the form for user creation.
    """

    base_username = State()  # State for base username
    start_number = State()  # State for start number
    how_much = State()  # State for amount
    data_limit = State()  # State for data limit
    date_limit = State()  # State for date limit
    status = State()  # State for user status
    admin = State()  # State for admin status
    inbounds = State()  # State for inbounds
