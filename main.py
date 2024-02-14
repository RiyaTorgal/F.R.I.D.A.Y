import speech_recognition as sr
import pyttsx3
import app

r = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"You said {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that")
            return ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    speak("Hello, I am FRIDAY, your Python-Powered AI Assistant")
    while True:
        command = listen()
        if "hello" in command:
            speak("Hi! How can I help you?")
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
                speak(f"{app_name} opened successfully.")
            break
        elif "thank you" in command:
            speak("Happy to help! Have a great day!")
            break
        else:
            speak("I'm sorry, I didn't understand that.")

if __name__ == "__main__": 
    print("Hello Riya!! :D")
    main()
