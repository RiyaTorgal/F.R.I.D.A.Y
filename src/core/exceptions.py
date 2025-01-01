class AssistantError(Exception):
    """Base exception class for assistant-related errors"""
    pass

class WeatherAPIError(AssistantError):
    """Raised when there's an error fetching weather data"""
    pass

class AppOperationError(AssistantError):
    """Raised when there's an error performing app operations"""
    pass