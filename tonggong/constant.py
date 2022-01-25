from .enum import IntEnum, StrEnum, enum


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
