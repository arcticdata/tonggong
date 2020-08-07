from .enum import IntEnum, StrEnum, enum


@enum.unique
class DatabaseAdapter(IntEnum):
    POSTGRESQL = 1  # 默认的数据库类型
    CLICKHOUSE = 2
    MYSQL = 3
    SPARK = 4

    @classmethod
    def choices(cls):
        return [
            (cls.POSTGRESQL.value, "PostgreSQL"),
            (cls.CLICKHOUSE.value, "ClickHouse"),
            (cls.MYSQL.value, "MySQL"),
            (cls.SPARK.value, "Spark"),
        ]


@enum.unique
class TimeUnit(IntEnum):
    SECONDS = 8
    MINUTES = 1
    HOURS = 2
    DAYS = 3
    WEEKS = 4
    MONTHS = 5
    QUARTERS = 6
    YEARS = 7

    @property
    def abbr(self) -> str:
        _abbr_map = {
            self.SECONDS: "s",
            self.MINUTES: "i",
            self.HOURS: "h",
            self.DAYS: "d",
            self.WEEKS: "w",
            self.MONTHS: "m",
            self.QUARTERS: "q",
            self.YEARS: "y",
        }
        return _abbr_map[self.value]


@enum.unique
class TimeUnitAbbr(StrEnum):
    SECONDS = "s"
    MINUTES = "i"
    HOURS = "h"
    DAYS = "d"
    WEEKS = "w"
    MONTHS = "m"
    QUARTERS = "q"
    YEARS = "y"

    @property
    def time_unit(self) -> TimeUnit:
        _time_unit_map = {
            self.SECONDS: TimeUnit.SECONDS,
            self.MINUTES: TimeUnit.MINUTES,
            self.HOURS: TimeUnit.HOURS,
            self.DAYS: TimeUnit.DAYS,
            self.WEEKS: TimeUnit.WEEKS,
            self.MONTHS: TimeUnit.MONTHS,
            self.QUARTERS: TimeUnit.QUARTERS,
            self.YEARS: TimeUnit.YEARS,
        }
        return _time_unit_map[self.value]
