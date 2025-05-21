import gradio as gr
from huggingface_hub import InferenceClient
from gtts import gTTS
import tempfile

client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

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

    response = client.text_generation(
        prompt,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.0,
        do_sample=True
    )

    response = response.strip().split("<|assistant|>")[-1].strip()
    history.append((message, response))
    audio_path = speak_text(response)
    return history, history, audio_path

with gr.Blocks() as demo:
    gr.Markdown("# Sambit AI 🤖")
    chatbot = gr.Chatbot([], label="Chat with AI", type="messages")
    msg = gr.Textbox(label="Type your message here", placeholder="Ask me anything...", scale=7)
    audio_output = gr.Audio(label="AI Voice", interactive=False)

    clear = gr.Button("🧹 Clear Chat")

    state = gr.State([])

    msg.submit(respond, [msg, state], [chatbot, state, audio_output])
    clear.click(lambda: ([], [], None), None, [chatbot, state, audio_output])

# ✅ Required to make it work on Hugging Face
demo.launch()

