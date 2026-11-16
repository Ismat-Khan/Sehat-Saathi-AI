import streamlit as st
from groq import Groq


def get_groq_client():
    """Create a secure Groq API client."""

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return None

    if not api_key:
        return None

    return Groq(api_key=api_key)


# Text generation model
TEXT_MODEL = "openai/gpt-oss-120b"

# Image understanding model
VISION_MODEL = "qwen/qwen3.8-27b"

# Speech recognition model
VOICE_MODEL = "whisper-large-v3-turbo"


def generate_response(messages, model=TEXT_MODEL):
    """Generate an AI response using Groq."""

    client = get_groq_client()

    if client is None:
        return "Groq API key is missing. Please configure Streamlit Secrets."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_completion_tokens=1500
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI service error: {str(error)}"
