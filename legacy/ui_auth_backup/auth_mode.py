from enum import Enum


class AuthMode(str, Enum):
    LOGIN = "login"
    RECOVERY = "recovery"
    REGISTER = "register"
