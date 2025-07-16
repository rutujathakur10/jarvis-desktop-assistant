import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os
import webbrowser
import pyjokes
import threading
import random

# Set up the text-to-speech engine
engine = pyttsx3.init()

# Speak out loud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to user's voice and convert to text
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1
        try:
            log("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5)
            log("🔎 Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            log(f"👤 You said: {command}")
            return command.lower()
        except:
            log("⚠️ Didn't catch that. Please try again.")
            return ""

# Display output in the text area
def log(message):
    output_text.configure(state='normal')
    output_text.insert(tk.END, message + "\n")
    output_text.configure(state='disabled')
    output_text.see(tk.END)

# Understand and perform the command
def process_command(command):
    if not command:
        return

    if any(word in command for word in ['wikipedia', 'who is', 'what is']):
        speak("Searching Wikipedia...")
        for phrase in ["wikipedia", "who is", "what is"]:
            command = command.replace(phrase, '')
        try:
            info = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            log(info)
            speak(info)
        except:
            speak("Sorry, no results found.")

    elif 'open notepad' in command:
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif 'open chrome' in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            speak("Opening Chrome")
            os.startfile(chrome_path)
        else:
            speak("Chrome is not installed in the default location.")

    elif 'open calculator' in command:
        speak("Opening Calculator")
        os.system("calc.exe")

    elif 'open file explorer' in command:
        speak("Opening File Explorer")
        os.system("explorer")

    elif 'open word' in command:
        word_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        if os.path.exists(word_path):
            speak("Opening Word")
            os.startfile(word_path)
        else:
            speak("Word is not installed in the default location.")

    elif 'time' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        log(f"🕒 Time: {now}")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        log("😂 " + joke)

    elif 'greet me' in command:
        greetings = ["Hello there!", "Hi, how can I help you?", "Hey! Ready to assist you.", "Greetings, my friend!"]
        greeting = random.choice(greetings)
        speak(greeting)
        log(greeting)

    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'open instagram' in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif 'search for' in command:
        query = command.replace("search for", "")
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        app.quit()

    else:
        speak("Let me Google that.")
        webbrowser.open(f"https://www.google.com/search?q={command}")

# Run assistant in a separate thread
def start_listening():
    threading.Thread(target=run_assistant).start()

def run_assistant():
    command = take_command()
    process_command(command)

# Button actions for quick features
def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")
    log(f"🕒 Time: {now}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    log("😂 " + joke)

def greet():
    greet_text = "Hello! I am Jarvis. How can I help you today?"
    speak(greet_text)
    log(greet_text)

# Build the GUI
app = tk.Tk()
app.title("Jarvis - Virtual Assistant")
app.geometry("700x600")
app.config(bg="#1e1e1e")

# Header label
header = tk.Label(app, text="🧠 JARVIS - Your Virtual Desktop Assistant", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="#00ffcc")
header.pack(pady=10)

# Quick action buttons
button_frame = tk.Frame(app, bg="#1e1e1e")
button_frame.pack(pady=5)

listen_btn = tk.Button(button_frame, text="🎙 Start Listening", command=start_listening, font=("Arial", 12), bg="#007acc", fg="white", padx=10)
listen_btn.grid(row=0, column=0, padx=5)

time_btn = tk.Button(button_frame, text="🕒 Time", command=tell_time, font=("Arial", 12), bg="#007acc", fg="white", padx=10)
time_btn.grid(row=0, column=1, padx=5)

joke_btn = tk.Button(button_frame, text="😂 Joke", command=tell_joke, font=("Arial", 12), bg="#007acc", fg="white", padx=10)
joke_btn.grid(row=0, column=2, padx=5)

greet_btn = tk.Button(button_frame, text="👋 Greet Me", command=greet, font=("Arial", 12), bg="#007acc", fg="white", padx=10)
greet_btn.grid(row=0, column=3, padx=5)

# Output display area
output_text = scrolledtext.ScrolledText(app, height=25, state='disabled', wrap='word', font=("Consolas", 11), bg="#2b2b2b", fg="#e6e6e6")
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Start the GUI loop
app.mainloop()
