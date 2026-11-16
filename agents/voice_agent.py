
import re
import html
from io import BytesIO

import streamlit as st
from gtts import gTTS

from utils.llm_config import get_groq_client, VOICE_MODEL


def clean_text_for_speech(text):
    """
    Remove Markdown and formatting symbols before
    sending the response to text-to-speech.
    """

    if not text:
        return ""

    text = html.unescape(str(text))

    # Remove code block markers, but retain readable contents
    text = re.sub(r"```[\w+-]*", "", text)

    # Convert Markdown links to their visible labels
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove Markdown images
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)

    # Remove Markdown headings
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Remove bold and italic markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"__(.*?)__", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\*)\*(?!\s)(.*?)(?<!\s)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!_)_(?!\s)(.*?)(?<!\s)_(?!_)", r"\1", text)

    # Remove strikethrough markers
    text = text.replace("~~", "")

    # Remove horizontal separators
    text = re.sub(r"^\s*[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)

    # Remove Markdown table separator rows
    text = re.sub(
        r"^\s*\|?[\s:|-]+\|?\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Replace table pipes with natural pauses
    text = text.replace("|", ", ")

    # Remove bullet and numbered-list formatting
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[\.)]\s+", "", text, flags=re.MULTILINE)

    # Remove blockquote markers
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Remove standalone web addresses
    text = re.sub(r"https?://\S+", "", text)

    # Clean repeated punctuation and whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    return text.strip()


def transcribe_audio(audio_bytes, language="English"):

    client = get_groq_client()

    if client is None:
        return "Groq API key is missing. Please configure Streamlit Secrets."

    try:
        lang_code = "ur" if language == "Urdu" else "en"

        result = client.audio.transcriptions.create(
            file=("recording.wav", audio_bytes),
            model=VOICE_MODEL,
            language=lang_code
        )

        return result.text.strip()

    except Exception as error:
        return f"Voice recognition error: {error}"


def speak_response(text, language="English"):

    try:
        clean_text = clean_text_for_speech(text)

        if not clean_text:
            return None

        lang_code = "ur" if language == "Urdu" else "en"

        audio = BytesIO()

        speech = gTTS(
            text=clean_text,
            lang=lang_code,
            slow=False
        )

        speech.write_to_fp(audio)
        audio.seek(0)

        return audio.read()

    except Exception as error:
        print("Speech generation error:", error)
        return None
