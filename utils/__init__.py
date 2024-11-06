"""
This module imports necessary components for database access and logging.
"""

from .statedb import SQLAlchemyStorage
from .log import BotLogger
from .config import EnvFile
from .lang import MessageTextsFile, KeyboardTextsFile
from .keys import BotKeyboards

logger = BotLogger("HolderBot").get_logger()
EnvSettings = EnvFile()
MessageTexts = MessageTextsFile()
KeyboardTexts = KeyboardTextsFile()
Storage = SQLAlchemyStorage()


__all__ = ["Storage", "logger", "KeyboardTexts", "MessageTexts", "BotKeyboards"]
