
import streamlit as st
import base64
from groq import Groq

TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.8-27b"
VOICE_MODEL = "whisper-large-v3-turbo"


def get_groq_client():
    try:
        key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=key)
    except Exception:
        return None


def generate_response(messages, model=TEXT_MODEL):
    client = get_groq_client()

    if client is None:
        return "Groq API key is missing. Configure Streamlit Secrets."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_completion_tokens=1500
        )
        return response.choices[0].message.content

    except Exception as error:
        return f"AI service error: {error}"


def analyze_image(image_bytes, prompt, language="English"):
    client = get_groq_client()

    if client is None:
        return "Groq API key is missing."

    try:
        encoded = base64.b64encode(image_bytes).decode("utf-8")

        content = [
            {
                "type": "text",
                "text": prompt + "\nRespond in " + language
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/jpeg;base64," + encoded
                }
            }
        ]

        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=0.2,
            max_completion_tokens=1500
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"Image analysis error: {error}"
