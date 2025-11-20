# ✈️ SkyFlow Flight Manager

### 📌 Overview  
SkyFlow is a cutting-edge application for managing flight operations, focusing on aircraft, ticketing, and user profiles. 
Designed for airlines and airport authorities, it enhances operational efficiency and improves passenger experience through digital solutions.

### ✨ Features  
- **Aircraft Management**: CRUD operations for aircraft details.
- **Flight Scheduling**: Manage flight timings and statuses.
- **Ticket Booking**: Allow users to book, cancel, and view tickets.
- **User Profiles**: Personalized management of user accounts.
- **Analytics**: Data-driven insights for flight trends.
- **Image Management**: Upload features for flight-related images.

### 💻 Tech Stack  
- **Languages**: C#
- **Framework**: .NET 8
- **ORM**: Entity Framework Core

### 🏗 Architecture  
Built on the MVC (Model-View-Controller) design pattern, the application separates data management, user interface, and request handling for maintainability and scalability.

### 📂 Folder Structure  
```
Flight_System/
├── AppServer/
│   ├── API/
│   │   ├── AircraftController.cs
│   │   ├── FlightController.cs
│   │   ├── TicketController.cs
│   │   └── UserController.cs
│   ├── Data/
│   │   └── DBContext.cs
│   ├── Models/
│   │   ├── Aircraft.cs
│   │   ├── Flight.cs
│   │   ├── Ticket.cs
│   │   └── User.cs
└── appsettings.json
```

### ▶️ How to Run  
To launch the SkyFlow application, execute:  
```bash
dotnet run
```

### 📸 Suggested Screenshots  
- **Admin Panel**
- **Analytics / Charts Page**
- **Prediction Feature**
- **Upload Page**