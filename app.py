# import os
# import webbrowser
# from datetime import datetime
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# api = os.environ.get("API_KEY")

# def open_website(url):
#     webbrowser.open(url)

# def open_app(app_name):
#     if app_name.lower() == "settings":
#         try:
#             os.startfile("ms-settings:")
#             print("Settings opened successfully.")
#         except Exception as e:
#             print(f"Error opening Settings: {e}")
#     else:
#         try:
#             os.startfile(app_name)
#             print(f"{app_name} opened successfully.")
#         except Exception as e:
#             print(f"Error opening {app_name}: {e}")

# def date_time():
#     now = datetime.now()
#     c_time = now.strftime("%H:%M")
#     c_date = now.strftime("%Y-%m-%d")
#     return c_time, c_date

# def calc(x):
#     try:
#         result = eval(x)
#         return result
#     except Exception as e:
#         return f"ERROR: {e}"

# def weather(city):
#     URL = "https://api.openweathermap.org/data/2.5/weather"
#     param = {
#         'q': city,
#         'appid': api,
#         'units': 'metric'
#     }
#     try:
#         res = requests.get(URL,params=param)
#         data = res.json()
#         if res.status_code == 200:
#             weatherData = data['weather'][0]['description']
#             tempData = data['main']['temp']
#             temp_min = data['main']['temp_min']
#             temp_max = data['main']['temp_max']
#             return f"The weather of {city} is {weatherData}. The current temperature is {tempData}°C. The high for today is {temp_max}°C, and the low is {temp_min}°C." 
#     except Exception as e:
#         return f"Error fetching the informtion: {e}"

import os
import webbrowser
from datetime import datetime
import requests
from typing import Tuple, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class WeatherData:
    description: str
    temperature: float
    temp_min: float
    temp_max: float
    city: str

    def __str__(self) -> str:
        return (f"The weather of {self.city} is {self.description}. "
                f"The current temperature is {self.temperature}°C. "
                f"The high for today is {self.temp_max}°C, and the low is {self.temp_min}°C.")

class AssistantError(Exception):
    """Base exception class for assistant-related errors"""
    pass

class WeatherAPIError(AssistantError):
    """Raised when there's an error fetching weather data"""
    pass

class AppOperationError(AssistantError):
    """Raised when there's an error performing app operations"""
    pass

class Assistant:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        if not self.api_key:
            raise AssistantError("API key not found in environment variables")
        
    def open_website(self, url: str) -> None:
        """Open website with error handling and URL validation"""
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        try:
            webbrowser.open(url)
        except Exception as e:
            raise AppOperationError(f"Failed to open website: {e}")

    def open_app(self, app_name: str) -> None:
        """Open application with improved error handling"""
        try:
            if app_name.lower() == "settings":
                os.startfile("ms-settings:")
            else:
                os.startfile(app_name)
        except Exception as e:
            raise AppOperationError(f"Failed to open {app_name}: {e}")

    def get_datetime(self) -> Tuple[str, str]:
        """Get current time and date"""
        now = datetime.now()
        return now.strftime("%H:%M"), now.strftime("%Y-%m-%d")

    def calculate(self, expression: str) -> float:
        """Safe mathematical expression evaluation"""
        # Whitelist of allowed characters for basic arithmetic
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            raise ValueError("Invalid characters in expression")
        try:
            result = eval(expression, {"__builtins__": {}})
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

    def get_weather(self, city: str) -> WeatherData:
        """Get weather data with improved error handling and data validation"""
        URL = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            return WeatherData(
                description=data['weather'][0]['description'],
                temperature=data['main']['temp'],
                temp_min=data['main']['temp_min'],
                temp_max=data['main']['temp_max'],
                city=city
            )
        except requests.RequestException as e:
            raise WeatherAPIError(f"Failed to fetch weather data: {e}")
        except (KeyError, IndexError) as e:
            raise WeatherAPIError(f"Invalid weather data format: {e}")