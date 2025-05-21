import os
import requests
import gradio as gr
from gtts import gTTS
import tempfile


TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_MODEL = "meta-llama/Llama-3-70B-Instruct"

def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

def together_generate(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": TOGETHER_MODEL,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "repetition_penalty": 1.0
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        return "⚠️ API error: " + response.text

def respond(message, history):
    history = history or []
    prompt = ""
    for user_msg, bot_msg in history:
        prompt += f"<|user|> {user_msg}\n<|assistant|> {bot_msg}\n"
    prompt += f"<|user|> {message}\n<|assistant|>"

    response = together_generate(prompt)
    history.append((message, response))
    audio_path = speak_text(response)
    return history, history, audio_path

with gr.Blocks() as demo:
    gr.Markdown("# Sambit AI 🤖")
    chatbot = gr.Chatbot([], label="Chat with AI", type="messages")
    msg = gr.Textbox(label="Type your message here", placeholder="Ask me anything...")
    audio_output = gr.Audio(label="AI Voice", interactive=False)
    clear = gr.Button("Clear Chat")
    state = gr.State([])

    msg.submit(respond, [msg, state], [chatbot, state, audio_output])
    clear.click(lambda: ([], [], None), None, [chatbot, state, audio_output])

demo.queue()  
