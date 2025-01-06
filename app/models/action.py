from enum import Enum


class ActionTypes(str, Enum):
    ADD_SERVICE = "add service"
    DELETE_SERVICE = "delete service"
