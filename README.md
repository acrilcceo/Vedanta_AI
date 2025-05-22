# Sambit AI (Gradio + Together API)

This is a chatbot powered by [Together.ai](https://www.together.ai/) and the Mixtral 8x7B model, deployed with Gradio.

## 🔧 Setup

1. Create a new Space on Hugging Face → Gradio template.
2. Add your Together API key in the **Settings > Secrets** tab as:

```
TOGETHER_API_KEY=your_api_key_here
```

3. Upload these files or the full ZIP.

## 🚀 Model Used
- Model: `mistralai/Mixtral-8x7B-Instruct-v0.1`
- Provider: [Together.ai](https://docs.together.ai/docs/inference)

## 🎙 Usage

Just ask anything! Sambit AI will respond with answers from the Together inference API.