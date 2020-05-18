from .enum import IntEnum, enum


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

    def get_abbreviation(self) -> str:
        return {
            self.SECONDS.value: "s",
            self.MINUTES.value: "i",
            self.HOURS.value: "h",
            self.DAYS.value: "d",
            self.WEEKS.value: "w",
            self.MONTHS.value: "m",
            self.QUARTERS.value: "q",
            self.YEARS.value: "y",
        }.get(self.value)
