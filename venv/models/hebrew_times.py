from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class DateDetails:
    def __init__(self, gregorian_date: datetime, hebrew_date: str, day_of_week: int, is_holiday: bool,
                shabbat_start: datetime, shabbat_end: datetime,
                parasha: str, holiday_name: Optional[str] = None,
                holiday_start: Optional[datetime] = None, holiday_end: Optional[datetime] = None):
        self.hebrew_date = hebrew_date
        self.gregorian_date = gregorian_date
        self.day_of_week = day_of_week
        self.parasha = parasha
        self.is_holiday = is_holiday
        self.holiday_name = holiday_name
        self.shabbat_start = shabbat_start
        self.shabbat_end = shabbat_end
        self.holiday_start = holiday_start
        self.holiday_end = holiday_end

    def to_server_format(self):
        return {
            "hebrewDate": self.hebrew_date,
            "gregorianDate": self.gregorian_date.isoformat(),
            "dayOfWeek": self.day_of_week,
            "parsha": self.parasha,
            "isHoliday": self.is_holiday,
            "holidayName": self.holiday_name,
            "nextShabbatStart": self.shabbat_start.isoformat(),
            "nextShabbatEnd": self.shabbat_end.isoformat(),
            "holidayStart": self.holiday_start.isoformat() if self.holiday_start else None,
            "HolidayEnd": self.holiday_end.isoformat() if self.holiday_end else None
        }

    @classmethod
    def to_client_format(cls, server_dict):
        return cls(
            gregorian_date=datetime.fromisoformat(server_dict["gregorianDate"]),
            hebrew_date=server_dict["hebrewDate"],
            day_of_week=server_dict["dayOfWeek"],
            is_holiday=server_dict["isHoliday"],
            shabbat_start=datetime.fromisoformat(server_dict["nextShabbatStart"]),
            shabbat_end=datetime.fromisoformat(server_dict["nextShabbatEnd"]),
            parasha=server_dict["parsha"],
            holiday_name=server_dict.get("holidayName"),
            holiday_start=datetime.fromisoformat(server_dict["holidayStart"]) if server_dict.get("holidayStart") else None,
            holiday_end=datetime.fromisoformat(server_dict["holidayEnd"]) if server_dict.get("HolidayEnd") else None
        )