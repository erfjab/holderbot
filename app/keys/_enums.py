from enum import Enum


class Pages(str, Enum):
    HOME = "home"
    SERVERS = "servers"
    MENU = "menu"
    USERS = "users"
    ACTIONS = "actions"
    UPDATE = "update"


class Actions(str, Enum):
    LIST = "list"
    INFO = "info"
    CREATE = "create"
    MODIFY = "modify"


class YesOrNot(str, Enum):
    YES = "yes"
    NO = "no"
