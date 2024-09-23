namespace AppServer.Models
{
    public class Flight_Details
    {
        public string Season { get; set; }
        public int FlightDistance { get; set; }
        public int FlightDuration { get; set; }
        public int DepartureAirportCongestion { get; set; }
        public int ArrivalAirportCongestion { get; set; }
        public string DayOfWeek { get; set; }
        public string TimeOfFlight { get; set; }
        public string ScheduledDepartureTime { get; set; }
        public string ActualDepartureTime { get; set; }
        public int DepartureDelay { get; set; }
        public double Temperature { get; set; }
        public double Visibility { get; set; }
        public double WindSpeed { get; set; }
        public string WeatherEvent { get; set; }
    }
}


