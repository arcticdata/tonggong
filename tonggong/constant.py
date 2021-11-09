from .enum import IntEnum, StrEnum, enum


@enum.unique
class DatabaseAdapter(IntEnum):
    POSTGRESQL = 1  # 默认的数据库类型
    CLICKHOUSE = 2
    MYSQL = 3
    SPARK_SQL = 4
    ELASTICSEARCH_QUERY = 5
    ELASTICSEARCH_SQL = 6
    MYSQL_5_7 = 7
    KYLIN = 8
    ORACLE = 9
    SQL_SERVER_2008 = 10
    TINGYUN = 11
    EXCEL = 12
    KYLIGENCE = 13
    APACHE_DORIS = 14
    GREENPLUM = 15
    SQL_SERVER_2012 = 16
    MONGODB_5_0 = 17

    @classmethod
    def choices(cls):
        return [
            (cls.POSTGRESQL.value, "PostgreSQL"),
            (cls.CLICKHOUSE.value, "ClickHouse"),
            (cls.MYSQL.value, "MySQL 8.0"),
            (cls.MYSQL_5_7.value, "MySQL 5.7"),
            (cls.SPARK_SQL.value, "Spark SQL"),
            (cls.ELASTICSEARCH_QUERY.value, "Elasticsearch Query"),
            (cls.ELASTICSEARCH_SQL.value, "Elasticsearch SQL"),
            (cls.KYLIN.value, "Apache Kylin"),
            (cls.ORACLE.value, "Oracle"),
            (cls.TINGYUN.value, "Tingyun"),
            (cls.EXCEL.value, "Excel"),
            (cls.KYLIGENCE.value, "Kyligence"),
            (cls.APACHE_DORIS.value, "Apache Doris"),
            (cls.GREENPLUM.value, "Greenplum"),
            (cls.SQL_SERVER_2008.value, "Microsoft SQL Server 2008"),
            (cls.SQL_SERVER_2012.value, "Microsoft SQL Server 2012"),
            (cls.MONGODB_5_0.value, "MongoDB 5.0")
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
            self.MINUTES: "m",
            self.HOURS: "h",
            self.DAYS: "d",
            self.WEEKS: "w",
            self.MONTHS: "M",
            self.QUARTERS: "Q",
            self.YEARS: "y",
        }
        return _abbr_map[self.value]


@enum.unique
class TimeUnitAbbr(StrEnum):
    """
    ref: https://momentjs.com/docs/#/manipulating/add/
    """

    SECONDS = "s"
    MINUTES = "m"
    HOURS = "h"
    DAYS = "d"
    WEEKS = "w"
    MONTHS = "M"
    QUARTERS = "Q"
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
