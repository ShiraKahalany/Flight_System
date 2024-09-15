namespace AppServer.Models;
using System;

public class MyDate
{
    public string? HebrewDate { get; set; }

    public DateTime GregorianDate { get; set; }

    public DayOfWeek DayOfWeek { get; set; }

    public string? Parsha { get; set; }

    public bool IsHoliday { get; set; }

    public DateTime NextShabbatStart { get; set; }

    public DateTime NextShabbatEnd { get; set; }

    public DateTime? HolidayStart { get; set; }

    public DateTime? HolidayEnd { get; set; }

    // Constructor
    public MyDate(string hebrewDate, DateTime gregorianDate, DayOfWeek dayOfWeek, string parsha, bool isHoliday,
                  DateTime nextShabbatStart, DateTime nextShabbatEnd, DateTime? holidayStart = null, DateTime? holidayEnd = null)
    {
        HebrewDate = hebrewDate;
        GregorianDate = gregorianDate;
        DayOfWeek = dayOfWeek;
        Parsha = parsha;
        IsHoliday = isHoliday;
        NextShabbatStart = nextShabbatStart;
        NextShabbatEnd = nextShabbatEnd;
        HolidayStart = holidayStart;
        HolidayEnd = holidayEnd;
    }

}

