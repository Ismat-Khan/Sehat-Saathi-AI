
from utils.llm_config import generate_response, analyze_image
from utils.language import get_language_instruction


def analyze_report(content, language="English", is_image=False):

    instruction = get_language_instruction(language)

    prompt = """
    You are a medical report explanation assistant.

    Explain:
    1. Type of report
    2. Important findings
    3. Medical terminology
    4. Abnormal values, if available
    5. Questions the patient should ask their doctor

    Never claim a confirmed diagnosis.
    Do not invent missing test values.
    For X-rays, explain only visible observations.
    State that a radiologist must interpret the image.
    """

    if is_image:
        return analyze_image(
            content,
            instruction + prompt,
            language
        )

    return generate_response([
        {
            "role": "user",
            "content": instruction + prompt +
                       "\n\nREPORT:\n" + content
        }
    ])
