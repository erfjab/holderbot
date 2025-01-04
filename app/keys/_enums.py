from enum import Enum


class Pages(str, Enum):
    HOME = "home"
    SERVERS = "servers"


class Actions(str, Enum):
    LIST = "list"
    INFO = "info"
    CREATE = "create"
    MODIFY = "modify"
