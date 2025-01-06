from enum import Enum


class ActionTypes(str, Enum):
    ADD_CONFIG = "add config"
    DELETE_CONFIG = "delete config"
