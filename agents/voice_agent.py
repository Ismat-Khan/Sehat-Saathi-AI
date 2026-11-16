
from groq import Groq
import streamlit as st
from gtts import gTTS
from io import BytesIO
from utils.llm_config import get_groq_client, VOICE_MODEL


def transcribe_audio(audio_bytes, language="English"):

    client = get_groq_client()

    if client is None:
        return "Groq API key is missing."

    try:
        lang_code = "ur" if language == "Urdu" else "en"

        result = client.audio.transcriptions.create(
            file=("recording.wav", audio_bytes),
            model=VOICE_MODEL,
            language=lang_code
        )

        return result.text

    except Exception as error:
        return f"Voice recognition error: {error}"


def speak_response(text, language="English"):

    try:
        lang_code = "ur" if language == "Urdu" else "en"

        audio = BytesIO()

        speech = gTTS(
            text=text,
            lang=lang_code
        )

        speech.write_to_fp(audio)
        audio.seek(0)

        return audio.read()

    except Exception:
        return None
