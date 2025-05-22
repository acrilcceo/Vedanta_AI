
import gradio as gr
from app import ask_ai

# GA4 tracking
tracking_script = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CLNDQ829HZ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-CLNDQ829HZ');
</script>
"""

with gr.Blocks() as demo:
    gr.HTML(tracking_script)
    gr.Markdown("## 🤖 Welcome to Sambit AI!")
    gr.ChatInterface(
        fn=ask_ai,
        title="Sambit AI 🤖 — Powered by Together & LLaMA 3",
        chatbot=gr.Chatbot(type="messages"),
        description="Ask anything. Sambit AI uses Together's Mixtral 8x7B model."
    )

demo.launch()
