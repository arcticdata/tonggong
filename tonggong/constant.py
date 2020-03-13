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
            (cls.POSTGRESQL.value, 'PostgreSQL'),
            (cls.CLICKHOUSE.value, 'ClickHouse'),
            (cls.MYSQL.value, 'MySQL'),
            (cls.SPARK.value, 'Spark'),
        ]


@enum.unique
class TimeUnit(IntEnum):
    HOURS = 0
    DAYS = 1
    WEEKS = 2
    MONTHS = 3
    QUARTERS = 4
    YEARS = 5
