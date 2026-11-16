
def check_emergency(text):

    emergency_keywords = [
        "chest pain",
        "difficulty breathing",
        "can't breathe",
        "severe bleeding",
        "unconscious",
        "stroke",
        "suicidal",
        "overdose",
        "seizure",
        "severe allergic reaction",
        "سانس نہیں آ رہا",
        "سینے میں شدید درد",
        "بے ہوش"
    ]

    text = text.lower()

    for keyword in emergency_keywords:
        if keyword in text:
            return True

    return False


def safety_notice(language="English"):

    if language == "Urdu":
        return """
        اگر علامات شدید یا خطرناک ہوں تو فوراً طبی مدد حاصل کریں۔
        یہ معلومات ڈاکٹر کے معائنے کا متبادل نہیں ہیں۔
        """

    return """
    This information is educational and does not replace
    professional medical advice. Seek urgent medical care
    for severe or emergency symptoms.
    """
