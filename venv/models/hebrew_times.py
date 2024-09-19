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


    @classmethod
    def to_client_format(cls, server_dict):
        
        def parse_datetime(dt_str):
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S") if dt_str else None
  
        return cls(
            gregorian_date=parse_datetime(server_dict["gregorianDate"]),
            hebrew_date=server_dict["hebrewDate"],
            day_of_week=server_dict["dayOfWeek"],
            is_holiday=server_dict["isHoliday"],
            shabbat_start=parse_datetime(server_dict["nextShabbatStart"]),
            shabbat_end=parse_datetime(server_dict["nextShabbatEnd"]),
            parasha=server_dict["parsha"],
            holiday_name=server_dict.get("holidayName") if server_dict.get("holidayName") else None,
            holiday_start=parse_datetime(server_dict["holidayStart"]) if server_dict.get("holidayStart") else None,
            holiday_end=parse_datetime(server_dict["holidayEnd"]) if server_dict.get("HolidayEnd") else None
        )