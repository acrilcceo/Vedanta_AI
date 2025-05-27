import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess

# ✅ Insert your OpenAI API key here
openai.api_key = "your-openai-api-key"

# 🎤 Initialize voice engine
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio).lower()
        print(f"🗣 You said: {query}")
        return query
    except:
        speak("Sorry, I couldn't understand that.")
        return ""

def gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a smart assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except:
        return "Couldn't connect to OpenAI."

def open_site(command, site_dict):
    for key, url in site_dict.items():
        if key in command:
            speak(f"Opening {key}")
            webbrowser.open(url)
            return True
    return False

def run_task(command):
    site_dict = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "netflix": "https://netflix.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "twitter": "https://twitter.com",
        "linkedin": "https://linkedin.com",
        "whatsapp": "https://web.whatsapp.com",
        "reddit": "https://reddit.com",
        "amazon": "https://amazon.in",
        "flipkart": "https://flipkart.com",
        "spotify": "https://open.spotify.com"
    }

    if open_site(command, site_dict):
        return

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {date}")

    elif "notepad" in command:
        speak("Opening Notepad")
        subprocess.Popen(["notepad.exe"])

    elif "calculator" in command:
        speak("Opening Calculator")
        subprocess.Popen(["calc.exe"])

    elif "paint" in command:
        speak("Opening Paint")
        subprocess.Popen(["mspaint.exe"])

    elif "command prompt" in command or "cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "shutdown" in command:
        speak("Shutting down")
        os.system("shutdown /s /t 1")

    elif "restart" in command:
        speak("Restarting your PC")
        os.system("shutdown /r /t 1")

    elif "log out" in command or "sign out" in command:
        speak("Signing you out")
        os.system("shutdown -l")

    elif "goodbye" in command or "exit" in command or "stop" in command:
        speak("Goodbye Sambit. Take care.")
        exit()

    else:
        # 🔥 Use GPT for general questions or unsupported tasks
        response = gpt_response(command)
        speak(response)

# 🧠 Main Loop
if __name__ == "__main__":
    speak("Hello Sambit. I am your personal assistant.")
    while True:
        query = listen()
        if query:
            run_task(query)


