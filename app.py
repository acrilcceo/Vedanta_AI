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

with gr.Blocks(theme=gr.themes.Base(), css=".gradio-container { max-width: 100% !important; padding: 1rem; }") as demo:
    with gr.Row():
        gr.Image(value="acrilc logo branding new name-16-16.png", height=60, show_label=False, container=False)
        gr.Markdown("## Sambit AI 🤖 — Powered by Acrilc", elem_id="title")

    chatbot = gr.Chatbot(label="Chat with Sambit AI", height=400)
    with gr.Row():
        msg = gr.Textbox(placeholder="Ask anything...", scale=4)
        send = gr.Button("Send", scale=1)

    clear = gr.Button("🧹 Clear chat")
    state = gr.State([])

    def respond(message, history):
        reply = ask_ai(message, history)
        history.append((message, reply))
        return history, ""

    send.click(respond, [msg, state], [chatbot, msg])
    msg.submit(respond, [msg, state], [chatbot, msg])
    clear.click(lambda: ([], ""), None, [chatbot, msg])

demo.launch()