from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

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

    def display_functions(self) -> dict:
        """Returns log of what fuction the assistant can perform till date"""
        return"""
Different function I can perform till date:
-------------------------------------------
1. Tell you current Date and/or Time
description: "Get current time",
example: "Friday tell me the time"
-------------------------------------------
2. Tell you the currect weather
description: "Get weather for a specific city",
example: "Friday tell me the weather of Pune",
params: ["city name"]
-------------------------------------------
3. Calculate any mathematical expression
description: "Perform mathematical calculations",
example: "Friday calculate 2 + 2",
supports: ["addition", "subtraction", "multiplication", "division"]
-------------------------------------------
4. I can open any desktop app or website on internet
"description": "Open websites or applications",
examples: "Friday open youtube.com" or "Friday open notepad"
-------------------------------------------
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