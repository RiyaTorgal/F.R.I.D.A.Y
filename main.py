# import app
# import data

# def main():
#     data.speak("Hello, I am FRIDAY, your Python-Powered AI Assistant")
#     choice = data.inputType()
#     while True:
#         command = choice()
#         if "hello" in command:
#             data.speak("Hi! How can I help you?")
#         elif command.startswith("open website"):
#             parts = command.split(" ", 2)
#             if len(parts) == 3:
#                 website = parts[2]
#                 url = f"https://{website}"
#                 try:
#                     app.open_website(url)
#                     print(f"Opening website: {url}")
#                 except Exception as e:
#                     print(f"Error opening website: {e}")
#             break
#         elif command.startswith("open app"):
#             part = command.split(" ",2)
#             if len(part) == 3:
#                 app_name = part[2]
#                 app.open_app(app_name)
#                 data.speak(f"{app_name} opened successfully.")
#             break
#         elif "tell me the time".lower() in command.lower():
#             time,_ = app.date_time()
#             data.speak(f"the current time is {time}")
#             break
#         elif "tell me the date".lower() in command.lower():
#             _, date = app.date_time()
#             data.speak(f"the current date is {date}")
#             break
#         elif "calculate".lower() in command.lower():
#             ex = command.split("calculate",1)[1].strip()
#             result = app.calc(ex)
#             data.speak(f"The result is: {result}")
#             break
#         elif "weather".lower() in command.lower():
#             parts = command.split("weather", 1)
#             if len(parts) > 1:
#                 city_parts = parts[1].strip()
#                 city = city_parts.split()
#                 city = city[1]
#             result = app.weather(city)
#             data.speak(result)
#             print(result)
#             break
#         elif "break" in command:
#             data.speak("Happy to help! Have a great day!")
#             break
#         else:
#             data.speak("I'm sorry, I didn't understand that.")

# if __name__ == "__main__": 
#     print("Hello Riya!! :D")
#     main()


# main.py
from typing import Optional
import app
import data
import signal
import sys
import re

class FridayAssistant:
    def __init__(self):
        self.assistant = app.Assistant()
        self.voice = data.VoiceAssistant()
        self.commands = {
            "time": self._handle_time,
            "date": self._handle_date,
            "calculate": self._handle_calculation,
            "weather": self._handle_weather,
            "open": self._handle_open,
            "exit": self._handle_exit,
        }
        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        """Setup handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\nReceived shutdown signal. Cleaning up...")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        """Cleanup resources before shutdown"""
        try:
            self.voice.speak("Goodbye!")
        except:
            pass
        print("\nThank you for using FRIDAY Assistant!")

    def _handle_open(self, command: str) -> str:
        """Handle both website and app opening commands"""
        parts = command.split(None, 2)
        if len(parts) < 2:
            return "Please specify what to open"
            
        target = parts[1]
        
        # Check if it's a website (contains domain-like structure)
        if '.' in target:
            try:
                self.assistant.open_website(target)
                return f"Opening website: {target}"
            except app.AppOperationError as e:
                return str(e)
        else:
            # Assume it's an application
            try:
                self.assistant.open_app(target)
                return f"Opening {target}"
            except app.AppOperationError as e:
                return str(e)

    def _handle_time(self, _: str) -> str:
        time, _ = self.assistant.get_datetime()
        return f"The current time is {time}"

    def _handle_date(self, _: str) -> str:
        _, date = self.assistant.get_datetime()
        return f"The current date is {date}"

    def _handle_calculation(self, command: str) -> str:
        # Extract the mathematical expression
        match = re.search(r'calculate\s+(.*)', command, re.IGNORECASE)
        if not match:
            return "Please provide a calculation (e.g., 'Friday calculate 2 + 2')"
        
        expression = match.group(1).strip()
        try:
            result = self.assistant.calculate(expression)
            return f"The result is: {result}"
        except ValueError as e:
            return str(e)

    def _handle_weather(self, command: str) -> str:
        # Extract city name
        match = re.search(r'weather\s+(?:of\s+|in\s+)?([a-zA-Z\s]+)', command, re.IGNORECASE)
        if not match:
            return "Please specify a city (e.g., 'Friday tell me the weather of London')"
        
        city = match.group(1).strip()
        try:
            weather_data = self.assistant.get_weather(city)
            return str(weather_data)
        except app.WeatherAPIError as e:
            return str(e)

    def _handle_exit(self, _: str) -> str:
        return "Happy to help! Have a great day!"

    def process_command(self, command: str) -> Optional[str]:
        """Process user commands and return appropriate response"""
        if not command:
            return None
            
        command = command.lower().strip()
        
        # Handle exit commands
        if command in ['exit', 'quit', 'bye']:
            return self._handle_exit(command)
            
        # Match command to handler
        for cmd_key, handler in self.commands.items():
            if cmd_key in command:
                return handler(command)
        
        return ("I'm sorry, I didn't understand that command. "
                "Please say 'help' to see available commands.")

    def run(self):
        """Main loop for the assistant"""
        # print("\n" + "="*50)
        # print("Welcome to FRIDAY - Your Python-Powered AI Assistant")
        # print("="*50 + "\n")
        print("")
        print("███████████ ███████████  ███████████████    █████████  █████ █████")
        print("░███░░░░░░█░░███░░░░░███░░███░░███░░░░███  ███░░░░░███░░███ ░░███") 
        print("░███   █ ░  ░███    ░███ ░███ ░███   ░░███░███    ░███ ░░███ ███")  
        print("░███████    ░██████████  ░███ ░███    ░███░███████████  ░░█████")   
        print("░███░░░█    ░███░░░░░███ ░███ ░███    ░███░███░░░░░███   ░░███")    
        print("░███  ░     ░███    ░███ ░███ ░███    ███ ░███    ░███    ░███")    
        print("█████       █████   ████████████████████  █████   █████   █████")   
        print("░░░░░       ░░░░░   ░░░░░░░░░░░░░░░░░░░░  ░░░░░   ░░░░░   ░░░░░")
        print("")
        print("Remember to start your commands with 'Friday'")
        print("For example: 'Friday tell me the time'")
        
        self.voice.speak("Hello, I am FRIDAY, your Python-Powered AI Assistant")
        input_method = self.voice.get_input_method()
        
        while True:
            try:
                command = input_method()
                if command in ["exit", "quit", "bye"]:
                    self.cleanup()
                    break
                    
                response = self.process_command(command)
                if response:
                    self.voice.speak(response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
                self.voice.speak("I encountered an error. Please try again.")

def main():
    try:
        assistant = FridayAssistant()
        assistant.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()