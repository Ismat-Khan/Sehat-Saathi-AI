
from utils.llm_config import generate_response
from utils.language import get_language_instruction


def create_diet_plan(
    age,
    goal,
    preference,
    allergies,
    conditions,
    language="English"
):

    instruction = get_language_instruction(language)

    prompt = f"""
    You are Sehat Saathi AI's nutrition education agent.

    Patient information:
    Age: {age}
    Health goal: {goal}
    Food preference: {preference}
    Allergies: {allergies}
    Health conditions: {conditions}

    Create a practical and balanced food plan.

    Include:
    1. Breakfast
    2. Lunch
    3. Dinner
    4. Healthy snacks
    5. Hydration suggestions
    6. Affordable Pakistani food alternatives
    7. General nutrition tips

    Safety:
    - Never recommend stopping medication.
    - Do not promise to cure any disease through diet.
    - Consider allergies.
    - Do not create restrictive diets for children.
    - For kidney disease, diabetes, pregnancy or other
      complex conditions, recommend a qualified dietitian.
    - Do not invent calorie or nutrient requirements.
    - Ask for a professional review where needed.
    """

    return generate_response([
        {
            "role": "user",
            "content": instruction + prompt
        }
    ])
