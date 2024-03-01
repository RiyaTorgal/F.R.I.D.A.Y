import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

def inputType():
    choice = input("choose input method (speak or type): ").lower()
    if choice == "speak":
        speak("Now listening")
        return listen
    elif choice == "type":
        return input("Enter your command: ").lower()
    else:
        print("Invalid choice")
        return input()


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

