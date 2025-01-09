from enum import Enum


class ActionTypes(str, Enum):
    ADD_CONFIG = "➕ Add Config"
    DELETE_CONFIG = "➖ Delete Config"
    DELETE_EXPIRED_USERS = "🗑 Delete Expired"
    DELETE_LIMITED_USERS = "🗑 Delete Limited"
    DELETE_USERS = "🗑 Delete Users"
