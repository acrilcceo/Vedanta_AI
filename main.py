
import gradio as gr
from app import ask_ai

tracking_script = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CLNDQ829HZ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-CLNDQ829HZ');
</script>

<style>
  @media only screen and (max-width: 768px) {
    .gradio-container {
      padding: 10px !important;
      font-size: 16px !important;
    }
    .gr-button {
      font-size: 16px !important;
      padding: 10px 15px !important;
    }
    .gr-chatbot {
      font-size: 16px !important;
    }
  }
</style>
"""

def create_app():
    with gr.Blocks() as demo:
        gr.HTML(tracking_script)
        gr.ChatInterface(
            fn=ask_ai,
            title="Vedanta AI 🤖 — Powered by Together & LLaMA 3",
            description="Ask anything. Vedanta AI uses Together's Mixtral 8x7B model."
        )
    return demo

demo = create_app()
demo.launch()
