
from utils.llm_config import generate_response
from utils.language import get_language_instruction


def create_summary(report, language="English"):

    instruction = get_language_instruction(language)

    prompt = """
    Create an easy-to-understand health summary.

    Include:
    1. Overall report overview
    2. Important findings
    3. Values outside the supplied reference ranges
    4. Medical terms explained
    5. Questions for the doctor

    Do not create missing information.
    Do not provide a diagnosis.
    """

    return generate_response([
        {
            "role": "user",
            "content": instruction + prompt +
                       "\n\nInformation:\n" + report
        }
    ])
