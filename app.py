import gradio as gr
import requests
import os

API_KEY = os.environ.get("TOGETHER_API_KEY")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def ask_ai(message, history):
    if not API_KEY:
        return "❌ API key not found. Please set it in Settings → Secrets."

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": "You are Sambit AI, a helpful assistant."}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": message})

    data = {
        "model": MODEL_NAME,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result['choices'][0]['message']['content']
        return reply
    except Exception as e:
        return f"❌ Error: {str(e)}"

gr.ChatInterface(
    fn=ask_ai,
    title="Sambit AI 🤖 — Powered by Acrilc",
    chatbot=gr.Chatbot(type="messages"),
    description="Ask anything. Sambit AI uses Together's Mixtral 8x7B model.",
).launch()