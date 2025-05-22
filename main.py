
import gradio as gr

# Your GA4 tracking script
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

# Simple chatbot function
def chatbot_response(message):
    return f"👋 Hi there! You said: {message}"

# Create the UI
with gr.Blocks() as demo:
    gr.HTML(tracking_script)
    gr.Markdown("## 🤖 Welcome to Sambit AI!")
    gr.ChatInterface(fn=chatbot_response)

# Launch the app (Gradio handles this on Spaces)
demo.launch()
