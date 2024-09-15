from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class DateDetails:
    def __init__(self, gregorian_date: datetime, hebrew_date: str, day_of_week: int, is_holiday: bool,
                shabbat_start: datetime, shabbat_end: datetime,
                parasha: str, holiday_name: Optional[str] = None,
                holiday_start: Optional[datetime] = None, holiday_end: Optional[datetime] = None):
        self.gregorian_date = gregorian_date
        self.hebrew_date = hebrew_date
        self.day_of_week = day_of_week
        self.is_holiday = is_holiday
        self.parasha = parasha
        self.holiday_name = holiday_name
        self.shabbat_start = shabbat_start
        self.shabbat_end = shabbat_end
        self.holiday_start = holiday_start
        self.holiday_end = holiday_end
