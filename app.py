
import gradio as gr
import os
import requests
from gtts import gTTS
import tempfile

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL = "meta-llama/Llama-3-70B-Instruct"

def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

def respond(message, history):
    history = history or []
    prompt = ""
    for user_msg, bot_msg in history:
        prompt += f"<|user|> {user_msg}\n<|assistant|> {bot_msg}\n"
    prompt += f"<|user|> {message}\n<|assistant|>"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "repetition_penalty": 1.1
    }
    response = requests.post("https://api.together.xyz/inference", headers=headers, json=payload)
    response_json = response.json()
    output_text = response_json.get("output", "").strip().split("<|assistant|>")[-1].strip()

    history.append((message, output_text))
    audio_path = speak_text(output_text)
    return history, history, audio_path

with gr.Blocks() as demo:
    gr.Markdown("# Sambit AI 🤖")
    chatbot = gr.Chatbot([], label="Chat with AI", type="messages")
    msg = gr.Textbox(label="Type your message here")
    audio_output = gr.Audio(label="AI Voice", interactive=False)
    clear = gr.Button("Clear Chat")
    state = gr.State([])

    msg.submit(respond, [msg, state], [chatbot, state, audio_output])
    clear.click(lambda: ([], [], None), None, [chatbot, state, audio_output])

demo.launch()
