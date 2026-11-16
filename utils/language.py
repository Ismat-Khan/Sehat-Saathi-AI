
def get_language_instruction(language):

    if language == "Urdu":
        return """
        Respond entirely in simple Urdu.
        Use understandable everyday Urdu.
        Explain difficult medical terms in simple words.
        """

    return """
    Respond in simple, clear English.
    Explain difficult medical terms in easy language.
    """


def translate_label(language, english, urdu):

    if language == "Urdu":
        return urdu

    return english
