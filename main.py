import app
import data

def main():
    data.speak("Hello, I am FRIDAY, your Python-Powered AI Assistant")
    choice = data.inputType()
    while True:
        command = choice()
        if "hello" in command:
            data.speak("Hi! How can I help you?")
        elif command.startswith("open website"):
            parts = command.split(" ", 2)
            if len(parts) == 3:
                website = parts[2]
                url = f"https://{website}"
                try:
                    app.open_website(url)
                    print(f"Opening website: {url}")
                except Exception as e:
                    print(f"Error opening website: {e}")
            break
        elif command.startswith("open app"):
            part = command.split(" ",2)
            if len(part) == 3:
                app_name = part[2]
                app.open_app(app_name)
                data.speak(f"{app_name} opened successfully.")
            break
        elif "tell me the time".lower() in command.lower():
            time,_ = app.date_time()
            data.speak(f"the current time is {time}")
            break
        elif "tell me the date".lower() in command.lower():
            _, date = app.date_time()
            data.speak(f"the current date is {date}")
            break
        elif "calculate".lower() in command.lower():
            ex = command.split("calculate",1)[1].strip()
            result = app.calc(ex)
            data.speak(f"The result is: {result}")
            break
        elif "weather".lower() in command.lower():
            parts = command.split("weather", 1)
            if len(parts) > 1:
                city_parts = parts[1].strip()
                city = city_parts.split()
                city = city[1]
            result = app.weather(city)
            data.speak(result)
            print(result)
            break
        elif "break" in command:
            data.speak("Happy to help! Have a great day!")
            break
        else:
            data.speak("I'm sorry, I didn't understand that.")

if __name__ == "__main__": 
    print("Hello Riya!! :D")
    main()
