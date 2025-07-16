import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user based on time
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your virtual assistant. How can I help you?")

# Function to take voice command from user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Waits until you pause while speaking
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return command.lower()

# Main function that runs the assistant loop
def run_assistant():
    wish_user()
    while True:
        command = take_command()

        if command == "none":
            continue

        # Wikipedia feature for who/what questions
        if 'wikipedia' in command or 'who is' in command or 'what is' in command:
            speak('Searching Wikipedia...')
            command = command.replace("wikipedia", "")
            command = command.replace("who is", "")
            command = command.replace("what is", "")
            try:
                result = wikipedia.summary(command, sentences=2)
                speak("According to Wikipedia")
                print(result)
                speak(result)
            except Exception as e:
                print("Error:", e)
                speak("Sorry, I couldn't find information on that.")

        elif 'stop' in command or 'exit' in command:
            speak("Goodbye!")
            break
        
        elif 'open notepad' in command:
            speak("Opening Notepad")
            os.system("notepad.exe")

        elif 'open chrome' in command:
            speak("Opening Google Chrome")
            try:
                os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            except FileNotFoundError:
                speak("Google Chrome not found at the default location. Please check the path.")

# Run the assistant
run_assistant()
