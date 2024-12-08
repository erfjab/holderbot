from .env.config import EnvSetup
from .lang.keyboard import KeyboardTextSetup
from .lang.message import MessageTextSetup

EnvFile = EnvSetup()
MessageText = MessageTextSetup()
KeyboardText = KeyboardTextSetup()

__all__ = ["EnvFile", "MessageText", "KeyboardText"]
