import enum


class Enum(enum.Enum):
    """ 常量，提供 choices 方法用于 Django Model Field """

    @classmethod
    def choices(cls) -> list:
        return [(_.value, _.value) for _ in cls]

    @classmethod
    def choice_values(cls) -> list:
        return [_.value for _ in cls]


class IntEnum(int, Enum):
    """ 整数型枚举 """


class StrEnum(str, Enum):
    """ 整数型枚举 """
