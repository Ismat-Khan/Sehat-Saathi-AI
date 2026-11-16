
import fitz


def extract_pdf_text(pdf_bytes):

    try:
        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text() + "\n"

        document.close()

        if not text.strip():
            return (
                "No selectable text found. "
                "This PDF may be scanned. "
                "Please upload its pages as images."
            )

        return text[:18000]

    except Exception as error:
        return f"PDF reading error: {error}"
