from enum import Enum


class Pages(str, Enum):
    HOME = "home"
    SERVERS = "servers"
    MENU = "menu"


class Actions(str, Enum):
    LIST = "list"
    INFO = "info"
    CREATE = "create"
    MODIFY = "modify"
