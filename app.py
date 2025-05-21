import os
import gradio as gr
from gtts import gTTS
import tempfile
from together import Together

# Load API key from Hugging Face Secrets
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=TOGETHER_API_KEY)

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

    response = client.chat.completions.create(
        model="meta-llama/Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
        top_p=0.95
    )

    answer = response.choices[0].message.content.strip()
    history.append((message, answer))
    audio_path = speak_text(answer)
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
