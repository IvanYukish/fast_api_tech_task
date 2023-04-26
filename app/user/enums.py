from enum import Enum


class UserData(str, Enum):
    admin = "admin"
    dev = "dev"
    mortal = "simple mortal"
