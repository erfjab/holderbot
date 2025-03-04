from enum import Enum


class Pages(str, Enum):
    HOME = "home"
    SERVERS = "servers"
    MENU = "menu"
    USERS = "users"
    ACTIONS = "actions"
    UPDATE = "update"
    TEMPLATES = "templates"
    STATS = "stats"


class Actions(str, Enum):
    LIST = "list"
    INFO = "info"
    CREATE = "create"
    MODIFY = "modify"
    SEARCH = "search"


class YesOrNot(str, Enum):
    YES_USAGE = "✅ Yes (reset usage)"
    YES_NORMAL = "✅ Yes (no reset/charge)"
    YES_CHARGE = "✅ Yes (charge)"
    YES = "✅ Yes"
    NO = "❌ No"
