import gradio as gr
import os
import requests

# ✅ Load API key from Hugging Face Secrets (set in Settings → Secrets)
API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def ask_ai(message):
    if not API_KEY:
        return "❌ API key not found. Please set it in Settings → Secrets."

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are Sambit AI, a helpful assistant."},
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
        return reply
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Gradio UI
chat_interface = gr.ChatInterface(fn=ask_ai, title="Sambit AI 🤖 — Powered by Together & LLaMA 3")

# ✅ Launch the app
if __name__ == "__main__":
    chat_interface.launch()
