import gradio as gr
import requests
import os
import speech_recognition as sr
import pyttsx3


TOGETHER_API_KEY = "92269fefcc8df100e2d395daab78ba62c0f3b64dbd477227020dce924e7821fe"

# Text-to-speech setup
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# 🎤 Speech-to-text function
def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Sorry, I could not understand your voice."
    except sr.RequestError:
        return "Could not request results from speech recognition service."

# 🤖 Call Together API
def call_together_api(message, history):
    messages = [{"role": "system", "content": "You are Sambit AI, a helpful assistant."}]
    for user_msg, ai_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})
    messages.append({"role": "user", "content": message})

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/Llama-3-70b-instruct",
            "messages": messages,
            "temperature": 0.7,
        }
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        speak(reply)
        return reply
    elif response.status_code == 429:
        return "Rate limit reached. Please wait a bit."
    else:
        return f"Error: {response.json()['error']['message']}"

# 🎤🎧 UI function (text + voice input)
def chatbot_interface(message, audio, history=[]):
    if audio is not None:
        message = transcribe_audio(audio)
    if message.strip() == "":
        return "", history
    reply = call_together_api(message, history)
    history.append((message, reply))
    return "", history

# 🎨 Dark theme UI
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🤖 Sambit AI\nAsk anything via text or voice")

    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(placeholder="Type your message here...", label="Text Input")
    audio_input = gr.Audio(sources="microphone", type="filepath", label="Or speak here")

    submit_btn = gr.Button("Send")

    state = gr.State([])

    submit_btn.click(chatbot_interface, inputs=[msg, audio_input, state], outputs=[msg, state])
    msg.submit(chatbot_interface, inputs=[msg, audio_input, state], outputs=[msg, state])

demo.launch()
