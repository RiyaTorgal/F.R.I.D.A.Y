import speech_recognition as sr
import pyttsx3
from typing import Callable, Optional, Union
from enum import Enum
from dataclasses import dataclass
from typing import List
import re

class InputMethod(Enum):
    SPEAK = "speak"
    TYPE = "type"

@dataclass
class Command:
    text: str
    timestamp: float
    source: InputMethod

class CommandParser:
    @staticmethod
    def parse_command(text: str) -> tuple[bool, str]:
        """
        Parse command to check if it starts with 'Friday' and extract the actual command
        Returns: (is_valid, command)
        """
        text = text.lower().strip()
        if text.startswith('friday'):
            return True, text[6:].strip()  # Remove 'friday' and extra spaces
        return False, text

    @staticmethod
    def normalize_command(command: str) -> str:
        """Normalize command text for consistent processing"""
        # Replace common variations of commands
        replacements = {
            'tell me the weather of': 'weather',
            'tell me the weather in': 'weather',
            'tell me weather of': 'weather',
            'tell me weather in': 'weather',
            'what is the weather in': 'weather',
            'what is the weather of': 'weather',
            'tell me the time': 'time',
            'what is the time': 'time',
            'tell me the date': 'date',
            'what is the date': 'date',
            'tell me today\'s date': 'date',
        }
        
        command = command.lower().strip()
        for old, new in replacements.items():
            command = command.replace(old, new)
            
        return command

class InputHistory:
    def __init__(self, max_size: int = 100):
        self.commands: List[Command] = []
        self.max_size = max_size

    def add(self, command: Command) -> None:
        self.commands.append(command)
        if len(self.commands) > self.max_size:
            self.commands.pop(0)

    def get_last_command(self) -> Optional[Command]:
        return self.commands[-1] if self.commands else None

class TypedInputHandler:
    def __init__(self):
        self.commands = {
            "help": self._show_help,
            "clear": self._clear_screen,
            "history": self._show_history,
            "exit": self._exit_handler
        }
        self.history = InputHistory()
        self.parser = CommandParser()
        self.active = True

    def _show_help(self) -> str:
        return """
Available Commands (start with 'Friday'):
---------------------------------------
- Friday open youtube.com         : Opens specified website
- Friday open notepad            : Opens specified application
- Friday tell me the time        : Shows current time
- Friday tell me the date        : Shows current date
- Friday calculate 2 + 2         : Calculates mathematical expression
- Friday tell me the weather of [city] : Shows weather for specified city

Additional Commands:
------------------
- help    : Shows this help message
- clear   : Clears the screen
- history : Shows command history
- exit    : Exits the assistant

Tips:
----
- Always start your commands with 'Friday'
- Speak clearly and naturally when using voice commands
- Type commands in a clear format when using text input
"""

    def _clear_screen(self) -> str:
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        return "Screen cleared."

    def _show_history(self) -> str:
        if not self.history.commands:
            return "No commands in history."
        
        history_text = "Command History:\n"
        for i, cmd in enumerate(self.history.commands[-10:], 1):
            history_text += f"{i}. {cmd.text}\n"
        return history_text

    def _exit_handler(self) -> str:
        self.active = False
        return "Exiting..."

    def get_input(self, prompt: str = "You: ") -> str:
        """Get input from user with command handling"""
        try:
            user_input = input(prompt).strip()
            
            # Handle built-in commands first
            if user_input.lower() in self.commands:
                return self.commands[user_input.lower()]()
            
            # Check if command starts with "Friday"
            is_valid, command = self.parser.parse_command(user_input)
            if not is_valid:
                return "Please start your command with 'Friday' (e.g., 'Friday tell me the time')"
            
            # Normalize command
            normalized_command = self.parser.normalize_command(command)
            
            # Add to history
            self.history.add(Command(
                text=user_input,
                timestamp=__import__('time').time(),
                source=InputMethod.TYPE
            ))
            
            return normalized_command
            
        except KeyboardInterrupt:
            return "exit"
        except EOFError:
            return "exit"

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.typed_handler = TypedInputHandler()
        self.history = InputHistory()
        self.parser = CommandParser()
        
    def get_input_method(self) -> Callable:
        """Get user's preferred input method"""
        while True:
            print("\nAvailable input methods:")
            print("1. type - Type commands using keyboard")
            print("2. speak - Use voice commands")
            
            choice = input("\nChoose input method (type/speak): ").lower().strip()
            
            if choice == InputMethod.SPEAK.value:
                self.speak("Now listening. Remember to start your command with 'Friday'")
                return self.listen
            elif choice == InputMethod.TYPE.value:
                print(self.typed_handler._show_help())
                return self.typed_handler.get_input
            
            print("Invalid choice. Please choose 'speak' or 'type'")

    def listen(self) -> str:
        """Listen for voice input with improved error handling"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                query = self.recognizer.recognize_google(audio, language="en-in")
                print(f"You said: {query}")
                
                # Check if command starts with "Friday"
                is_valid, command = self.parser.parse_command(query)
                if not is_valid:
                    self.speak("Please start your command with 'Friday'")
                    return ""
                
                # Normalize command
                normalized_command = self.parser.normalize_command(command)
                
                # Add to history
                self.history.add(Command(
                    text=query,
                    timestamp=__import__('time').time(),
                    source=InputMethod.SPEAK
                ))
                
                return normalized_command
                
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Error with speech recognition service: {e}"
            except Exception as e:
                return f"An error occurred: {e}"

    def speak(self, text: str) -> None:
        """Text-to-speech output"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()