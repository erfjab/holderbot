from enum import Enum


class ActionTypes(str, Enum):
    ADD_CONFIG = "add config"
    DELETE_CONFIG = "delete config"
    DELETE_EXPIRED_USERS = "del expired users"
    DELETE_LIMITED_USERS = "del limited users"
