import gradio as gr
from together import Together
from gtts import gTTS
import tempfile
import os

# Get your Together API key from Hugging Face secret
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)

# Text-to-speech with gTTS
def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Main chat function
def respond(message, history):
    history = history or []
    prompt = ""
    for user_msg, bot_msg in history:
        prompt += f"<|user|> {user_msg}\n<|assistant|> {bot_msg}\n"
    prompt += f"<|user|> {message}\n<|assistant|>"

    # Call Together API
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
        top_p=0.95
    )

    reply = response.choices[0].message.content.strip()
    history.append((message, reply))
    audio_path = speak_text(reply)
    return history, history, audio_path

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Sambit AI 🤖 — Powered by Together & LLaMA 3")

    chatbot = gr.Chatbot(label="Chat with AI")
    msg = gr.Textbox(label="Type your message here")
    audio_output = gr.Audio(label="AI Voice", interactive=False)
    clear = gr.Button("Clear Chat")
    state = gr.State([])

    msg.submit(respond, [msg, state], [chatbot, state, audio_output])
    clear.click(lambda: ([], [], None), None, [chatbot, state, audio_output])

demo.launch()
