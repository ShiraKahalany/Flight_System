# ✈️ Flight System

The Flight System is a robust application designed for managing various aspects of flight operations, including aircraft, tickets, and user information. It facilitates seamless interactions between airlines, passengers, and airport authorities. This system is ideal for airlines looking to digitize their operations, improve customer experience, and streamline ticketing processes.

## ✨ Features
- **Aircraft Management**: Add, update, and delete aircraft details.
- **Flight Scheduling**: Schedule and manage flight timings and statuses.
- **Ticket Booking**: Enable users to book, cancel, and view their tickets.
- **User Profiles**: Manage user registrations and profiles for a personalized experience.
- **Prediction Analytics**: Leverage data for predicting flight trends.
- **Image Uploads**: Allow users/admins to upload images related to flights.

## 🛠 Tech Stack
- **Languages**: C#
- **Frameworks**: .NET 8
- **Database**: Entity Framework Core
- **Architecture**: MVC (Model-View-Controller)

## 🏗 Architecture
The Flight System employs an MVC architecture, which separates the application into three interconnected components:

- **Model**: Represents the data structure, containing various entities such as `Aircraft`, `Flight`, `Ticket`, and `User`. This layer handles data operations, using Entity Framework Core for database interaction.
  
- **View**: Presents the user interface, allowing users to interact with the system. The View component retrieves data from the Model and displays it to the user.

- **Controller**: Acts as an intermediary between the Model and View, managing user requests and updating the Model based on user input before refreshing the View.

This clear separation of concerns ensures maintainability and scalability as the application grows.

## 📂 Folder Structure
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

## ▶️ Running the Project
To run the Flight System application, execute the following command:
```bash
dotnet run
```

## 🖼 Suggested Screenshots
- **Admin Panel**
- **Analytics / Charts Page**
- **Prediction Feature**
- **Upload Page**
