import os
import webbrowser

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