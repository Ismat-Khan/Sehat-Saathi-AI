
from utils.llm_config import generate_response, analyze_image
from utils.language import get_language_instruction
from tools.medicine_tools import search_medicine


def analyze_medicine(name, language="English"):

    instruction = get_language_instruction(language)

    database_info = search_medicine(name)

    prompt = f"""
    You are a medicine information assistant.

    Explain:
    1. Identified medicine
    2. Generic name
    3. General medical uses
    4. Common side effects
    5. Important warnings
    6. Questions to ask a pharmacist

    Use the database information below:
    {database_info}

    Never prescribe a dose.
    Never recommend starting or stopping medication.
    If the medicine is uncertain, clearly say so.
    Do not invent information.
    """

    return generate_response([
        {
            "role": "user",
            "content": instruction + prompt
        }
    ])


def analyze_medicine_image(image, language="English"):

    identification = analyze_image(
        image,
        """
        Read the medicine packaging.
        Identify visible brand name, generic name,
        strength and manufacturer if readable.
        Do not guess missing information.
        """
    )

    instruction = get_language_instruction(language)

    database_info = search_medicine(identification)

    return generate_response([
        {
            "role": "user",
            "content": instruction +
            f"""
            Medicine label identification:
            {identification}

            Reference database:
            {database_info}

            Explain the medicine and its precautions.
            Clearly state any uncertainty.
            Do not recommend a dose or replace a pharmacist.
            """
        }
    ])
