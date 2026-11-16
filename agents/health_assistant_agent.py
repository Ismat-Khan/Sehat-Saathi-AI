
from utils.llm_config import generate_response
from utils.language import get_language_instruction


def health_chat(question, history, language="English"):

    instruction = get_language_instruction(language)

    system_prompt = """
    You are Sehat Saathi AI, a friendly healthcare
    education assistant.

    Help users understand general health topics.

    Rules:
    - Use simple explanations.
    - Do not claim to diagnose diseases.
    - Do not prescribe medicines.
    - Never advise stopping prescribed medication.
    - Ask for clarification when needed.
    - Identify emergency warning signs.
    - Recommend professional medical advice when appropriate.
    """

    messages = [
        {
            "role": "system",
            "content": instruction + system_prompt
        }
    ]

    messages.extend(history[-8:])

    messages.append({
        "role": "user",
        "content": question
    })

    return generate_response(messages)
