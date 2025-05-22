import gradio as gr
from app import ask_ai

# GA4 tracking script (will go into HTML block)
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

# A wrapper function to inject the GA script and return the chatbot interface
def create_app():
    with gr.Blocks() as demo:
        gr.HTML(tracking_script)
        gr.ChatInterface(
            fn=ask_ai,
            title="Sambit AI 🤖 — Powered by Acrilc",
            description="Ask anything. Sambit AI uses Together's Mixtral 8x7B model."
        )
    return demo

demo = create_app()
demo.launch()
