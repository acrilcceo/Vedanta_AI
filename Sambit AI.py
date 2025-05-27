import tkinter as tk
from tkinter import scrolledtext
import requests
import speech_recognition as sr
import pyttsx3

# Replace with your Together API key
API_KEY = "92269fefcc8df100e2d395daab78ba62c0f3b64dbd477227020dce924e7821fe"
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Text-to-Speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Ask AI
def ask_ai(prompt):
    response_text.delete("1.0", tk.END)
    response_text.insert(tk.END, "Thinking...\n")

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are Sambit AI, a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, reply)
            speak(reply)
        elif response.status_code == 429:
            msg = "⚠️ Rate limit hit. Please wait and try again."
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, msg)
            speak(msg)
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, error_msg)
            speak("There was an error with the request.")
    except Exception as e:
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, f"Exception: {str(e)}")
        speak("Sorry, an error occurred.")

# From typed input
def ask_from_text():
    user_input = question_entry.get()
    if user_input.strip():
        ask_ai(user_input)

# From voice input
def ask_from_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, "🎤 Listening...\n")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

        question = recognizer.recognize_google(audio)
        question_entry.delete(0, tk.END)
        question_entry.insert(0, question)
        ask_ai(question)

    except sr.UnknownValueError:
        msg = "Sorry, I couldn't understand your voice."
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, msg)
        speak(msg)
    except sr.RequestError:
        msg = "Could not connect to speech recognition service."
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, msg)
        speak(msg)
    except Exception as e:
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, f"Error: {str(e)}")
        speak("Something went wrong while using the microphone.")

# 🌙 Dark mode colors
BG_COLOR = "#1e1e1e"
FG_COLOR = "#d4d4d4"
ENTRY_BG = "#2d2d2d"
BUTTON_BG = "#3a3a3a"
BUTTON_FG = "#ffffff"
HIGHLIGHT_COLOR = "#007acc"

# GUI Setup
window = tk.Tk()
window.title("Sambit AI - Ask Anything")
window.geometry("600x500")
window.configure(bg=BG_COLOR)

label = tk.Label(window, text="Ask Sambit AI anything:", bg=BG_COLOR, fg=FG_COLOR)
label.pack(pady=5)

question_entry = tk.Entry(window, width=80, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
question_entry.pack(pady=5)

button_frame = tk.Frame(window, bg=BG_COLOR)
button_frame.pack(pady=5)

ask_button = tk.Button(button_frame, text="📝 Ask", command=ask_from_text, bg=BUTTON_BG, fg=BUTTON_FG, activebackground=HIGHLIGHT_COLOR)
ask_button.pack(side=tk.LEFT, padx=10)

speak_button = tk.Button(button_frame, text="🎤 Speak", command=ask_from_voice, bg=BUTTON_BG, fg=BUTTON_FG, activebackground=HIGHLIGHT_COLOR)
speak_button.pack(side=tk.LEFT, padx=10)

response_text = scrolledtext.ScrolledText(window, height=18, width=70, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
response_text.pack(pady=10)
response_text.config(highlightbackground=BG_COLOR, highlightcolor=HIGHLIGHT_COLOR)

window.mainloop()
