from .env.config import EnvSetup
from .lang.keyboard import KeyboardTextSetup
from .lang.message import MessageTextSetup
from .log.log import LoggerSetup

EnvFile = EnvSetup()
MessageText = MessageTextSetup()
KeyboardText = KeyboardTextSetup()
logger = LoggerSetup("HolderBot").get_logger()

__all__ = ["EnvFile", "MessageText", "KeyboardText", "logger"]
