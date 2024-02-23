import os
import webbrowser
from datetime import datetime

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
    