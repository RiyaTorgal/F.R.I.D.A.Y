import os
import webbrowser
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

api = os.environ.get("API_KEY")

def open_website(url):
    webbrowser.open(url)

def open_app(app_name):
    if app_name.lower() == "settings":
        try:
            os.startfile("ms-settings:")
            print("Settings opened successfully.")
        except Exception as e:
            print(f"Error opening Settings: {e}")
    else:
        try:
            os.startfile(app_name)
            print(f"{app_name} opened successfully.")
        except Exception as e:
            print(f"Error opening {app_name}: {e}")

def date_time():
    now = datetime.now()
    c_time = now.strftime("%H:%M")
    c_date = now.strftime("%Y-%m-%d")
    return c_time, c_date

def calc(x):
    try:
        result = eval(x)
        return result
    except Exception as e:
        return f"ERROR: {e}"

def weather(city):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    param = {
        'q': city,
        'appid': api,
        'units': 'metric'
    }
    try:
        res = requests.get(URL,params=param)
        data = res.json()
        if res.status_code == 200:
            weatherData = data['weather'][0]['description']
            tempData = data['main']['temp']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            return f"The weather of {city} is {weatherData}. The current temperature is {tempData}°C. The high for today is {temp_max}°C, and the low is {temp_min}°C." 
    except Exception as e:
        return f"Error fetching the informtion: {e}"