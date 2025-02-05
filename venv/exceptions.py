# exceptions.py

class BaseCustomException(Exception):
    """Base class for custom exceptions"""
    pass

# User-related exceptions

class UserAlreadyExistsException(BaseCustomException):
    """Raised when attempting to create a user with an existing username."""
    pass

class UserNotFoundException(BaseCustomException):
    """Raised when a user is not found."""
    pass

class InvalidCredentialsException(BaseCustomException):
    """Raised when the provided credentials are invalid."""
    pass

class UserCreationException(BaseCustomException):
    """Raised when there's an error creating a new user."""
    pass

# Ticket-related exceptions
class TicketCreationException(BaseCustomException):
    """Raised when there's an error creating a new ticket."""
    pass

class TicketRetrievalException(BaseCustomException):
    """Raised when there's an error retrieving tickets."""
    pass

class TicketNotFoundException(BaseCustomException):
    """Raised when a ticket is not found."""
    pass

# Image recognition exceptions
class ImageAnalysisException(BaseCustomException):
    """Raised when there's an error analyzing an image."""
    pass


# Flight-related exceptions
class FlightCreationException(BaseCustomException):
    """Raised when there's an error creating a new flight."""
    pass

class FlightNotFoundException(BaseCustomException):
    """Raised when a flight is not found."""
    pass

class FlightRetrievalException(BaseCustomException):
    """Raised when there's an error retrieving flights."""
    pass

# Aircraft-related exceptions
class AircraftCreationException(BaseCustomException):
    """Raised when there's an error creating a new aircraft."""
    pass

class AircraftRetrievalException(BaseCustomException):
    """Raised when there's an error retrieving aircrafts."""
    pass

class AircraftNotFoundException(BaseCustomException):
    """Raised when an aircraft is not found."""
    pass

# Date details-related exceptions
class DateDetailsRetrievalException(BaseCustomException):
    """Raised when there's an error retrieving date details."""
    pass

class InvalidLocationException(BaseCustomException):
    """Raised when an invalid location is provided."""
    pass

# Generic exceptions
class NetworkException(BaseCustomException):
    """Raised when there's a network-related error."""
    pass

class UnexpectedErrorException(BaseCustomException):
    """Raised when an unexpected error occurs."""
    pass