
import streamlit as st
from PIL import Image
from io import BytesIO

from tools.report_tools import extract_pdf_text

from agents.medical_report_agent import analyze_report
from agents.medicine_agent import analyze_medicine_image, analyze_medicine
from agents.health_assistant_agent import health_chat
from agents.health_summary_agent import create_summary
from agents.diet_agent import create_diet_plan
from agents.safety_agent import check_emergency
from agents.voice_agent import transcribe_audio, speak_response


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Sehat Saathi AI",
    page_icon="💚",
    layout="wide"
)


# -----------------------------------
# THEME-AWARE DESIGN
# Supports Light, Dark and System themes
# -----------------------------------

st.markdown("""
<style>

/* Use Streamlit's active theme colors */
:root {
    --ssa-bg: var(--background-color, #F4F8F7);
    --ssa-secondary: var(--secondary-background-color, #E5F3EF);
    --ssa-text: var(--text-color, #20343A);
    --ssa-primary: var(--primary-color, #087F70);
}

/* Main application */
.stApp {
    background-color: var(--ssa-bg) !important;
    color: var(--ssa-text) !important;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--ssa-bg) !important;
}

/* Header */
[data-testid="stHeader"] {
    background-color: var(--ssa-bg);
}

/* All ordinary text follows the active theme */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: var(--ssa-text);
}

/* Main title */
.main-title {
    color: var(--ssa-primary) !important;
    font-size: 38px;
    font-weight: 800;
}

/* Subtitle */
.subtitle {
    color: var(--ssa-text) !important;
    opacity: 0.8;
    font-size: 16px;
}

/* Sidebar follows the active theme */
[data-testid="stSidebar"] {
    background-color: var(--ssa-secondary) !important;
}

/* Sidebar text */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [role="radiogroup"] * {
    color: var(--ssa-text) !important;
}

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    color: var(--ssa-primary) !important;
    font-weight: 800;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-testid="stChatInput"] textarea {
    background-color: var(--ssa-secondary) !important;
    color: var(--ssa-text) !important;
    border: 1px solid rgba(128, 128, 128, 0.45) !important;
    border-radius: 8px;
}

/* Input placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--ssa-text) !important;
    opacity: 0.6;
}

/* Select box */
[data-baseweb="select"] > div {
    background-color: var(--ssa-secondary) !important;
    color: var(--ssa-text) !important;
    border-color: rgba(128, 128, 128, 0.45) !important;
}

[data-baseweb="select"] * {
    color: var(--ssa-text) !important;
}

/* Input labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label,
.stFileUploader label {
    color: var(--ssa-text) !important;
    font-weight: 600;
}

/* Buttons: preserve Streamlit's theme-aware colors */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

/* Upload area */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--ssa-primary);
    border-radius: 12px;
    padding: 8px;
}

/* Chat messages: let Streamlit choose theme colors */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    border: 1px solid rgba(128, 128, 128, 0.25);
}

/* Alerts: preserve native light/dark contrast */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Links */
a {
    color: var(--ssa-primary) !important;
}

/* Dividers */
hr {
    border-color: rgba(128, 128, 128, 0.3);
}

/* Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.markdown("# 💚 Sehat Saathi AI")

    st.caption("Your Intelligent Healthcare Companion")

    language = st.selectbox(
        "🌐 Select Language / زبان منتخب کریں",
        ["English", "Urdu"],
        index=0 if st.session_state.language == "English" else 1
    )

    st.session_state.language = language

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Medical Report Analysis",
            "Medicine Scanner",
            "AI Health Chat",
            "Diet & Nutrition",
            "Health Summary"
        ]
    )

    st.divider()

    st.caption("Powered by Groq AI")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


# -----------------------------------
# LANGUAGE LABELS
# -----------------------------------

if language == "Urdu":

    welcome = "آپ کا صحت کا ساتھی"
    subtitle = "آپ کی صحت، آپ کی زبان، آپ کا ساتھی"
    description = "اپنی صحت کے بارے میں آسان معلومات حاصل کریں۔"

else:

    welcome = "Your Health Companion"
    subtitle = "Your Health, Your Language, Your Companion."
    description = "Understand your health with AI-powered assistance."


# -----------------------------------
# HOME PAGE
# -----------------------------------

if page == "Home":

    st.markdown(
        '<div class="main-title">💚 Sehat Saathi AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"### {welcome}")

    st.markdown(
        f'<div class="subtitle">{subtitle}</div>',
        unsafe_allow_html=True
    )

    st.write(description)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "🩻 **Medical Reports**\n\n"
            "Upload your medical reports or X-rays."
        )

        st.success(
            "💊 **Medicine Scanner**\n\n"
            "Understand medicine labels and information."
        )

        st.info(
            "🥗 **Diet & Nutrition**\n\n"
            "Get general personalized diet guidance."
        )

    with col2:

        st.success(
            "💬 **AI Health Chat**\n\n"
            "Ask healthcare-related questions."
        )

        st.info(
            "📋 **Health Summary**\n\n"
            "Create easy-to-understand health summaries."
        )

        st.success(
            "🎙️ **Voice Assistant**\n\n"
            "Speak with your healthcare assistant."
        )

    st.divider()

    st.warning(
        "Sehat Saathi AI provides educational information. "
        "It is not a replacement for doctors, radiologists, "
        "pharmacists or emergency medical services."
    )


# -----------------------------------
# MEDICAL REPORT ANALYSIS
# -----------------------------------

elif page == "Medical Report Analysis":

    st.title("🩻 Medical Report Analysis")

    st.write(
        "Upload an X-ray, medical image or PDF report."
    )

    uploaded_file = st.file_uploader(
        "Upload your medical file",
        type=["png", "jpg", "jpeg", "webp", "pdf"]
    )

    if uploaded_file:

        file_bytes = uploaded_file.getvalue()

        is_pdf = uploaded_file.name.lower().endswith(".pdf")

        if is_pdf:

            with st.spinner("Reading medical report..."):

                extracted_text = extract_pdf_text(file_bytes)

            st.subheader("Extracted Report Text")

            st.text_area(
                "Report content",
                extracted_text,
                height=200
            )

            if st.button("Analyze Medical Report"):

                with st.spinner("Analyzing report..."):

                    result = analyze_report(
                        extracted_text,
                        language
                    )

                    st.session_state.report_result = result

                st.subheader("Medical Explanation")
                st.write(result)

        else:

            st.image(
                file_bytes,
                caption="Uploaded medical image",
                width=500
            )

            if st.button("Analyze Medical Image"):

                with st.spinner("Analyzing image..."):

                    image = Image.open(
                        BytesIO(file_bytes)
                    ).convert("RGB")

                    buffer = BytesIO()

                    image.save(
                        buffer,
                        format="JPEG",
                        quality=85
                    )

                    result = analyze_report(
                        buffer.getvalue(),
                        language,
                        is_image=True
                    )

                    st.session_state.report_result = result

                st.subheader("AI Image Explanation")
                st.write(result)

        if st.button("Create Health Summary"):

            previous_result = st.session_state.get(
                "report_result",
                ""
            )

            if previous_result:

                with st.spinner("Creating summary..."):

                    summary = create_summary(
                        previous_result,
                        language
                    )

                st.subheader("Health Summary")
                st.write(summary)

            else:

                st.warning(
                    "Please analyze a report or image first."
                )


# -----------------------------------
# MEDICINE SCANNER
# -----------------------------------

elif page == "Medicine Scanner":

    st.title("💊 Medicine Information Scanner")

    st.write(
        "Upload a clear picture of your medicine packaging."
    )

    medicine_image = st.file_uploader(
        "Upload Medicine Picture",
        type=["png", "jpg", "jpeg", "webp"]
    )

    medicine_name = st.text_input(
        "Or enter medicine name manually"
    )

    if medicine_image:

        st.image(
            medicine_image,
            caption="Medicine image",
            width=350
        )

    if st.button("Identify Medicine"):

        if medicine_image or medicine_name.strip():

            with st.spinner("Checking medicine information..."):

                if medicine_image:

                    image = Image.open(
                        BytesIO(medicine_image.getvalue())
                    ).convert("RGB")

                    buffer = BytesIO()

                    image.save(
                        buffer,
                        format="JPEG"
                    )

                    result = analyze_medicine_image(
                        buffer.getvalue(),
                        language
                    )

                else:

                    result = analyze_medicine(
                        medicine_name,
                        language
                    )

            st.subheader("Medicine Information")
            st.write(result)

            st.warning(
                "Always verify medicine information with a pharmacist. "
                "Do not change medication based on AI output."
            )

        else:

            st.warning(
                "Please upload a medicine image or enter its name."
            )


# -----------------------------------
# AI HEALTH CHAT
# -----------------------------------

elif page == "AI Health Chat":

    st.title("💬 Sehat Saathi AI Assistant")

    st.write(
        "Ask your health questions or talk using your microphone."
    )

    # Display previous conversation

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # Text input

    question = st.chat_input(
        "Ask your health question..."
    )

    # Voice input

    audio = st.audio_input(
        "Or record your question"
    )

    if audio and st.button("Process Voice Message"):

        with st.spinner("Converting voice to text..."):

            question = transcribe_audio(
                audio.getvalue(),
                language
            )

        st.write("Recognized speech:")
        st.write(question)

    if question:

        if check_emergency(question):

            if language == "Urdu":

                st.error(
                    "ممکنہ طبی ایمرجنسی۔ "
                    "فوراً اپنے مقامی ایمرجنسی نمبر پر رابطہ کریں "
                    "یا قریبی ایمرجنسی ڈیپارٹمنٹ جائیں۔"
                )

            else:

                st.error(
                    "Possible medical emergency. Contact "
                    "your local emergency services or go to "
                    "the nearest emergency department immediately."
                )

        else:

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.spinner("Sehat Saathi AI is thinking..."):

                result = health_chat(
                    question,
                    st.session_state.messages[:-1],
                    language
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": result
            })

            st.rerun()

    if st.session_state.messages:

        last_message = st.session_state.messages[-1]

        if last_message["role"] == "assistant":

            if st.button("🔊 Speak Last Response"):

                with st.spinner("Generating voice..."):

                    audio_bytes = speak_response(
                        last_message["content"],
                        language
                    )

                if audio_bytes:

                    st.audio(
                        audio_bytes,
                        format="audio/mp3"
                    )

                else:

                    st.error("Voice generation failed.")


# -----------------------------------
# DIET AND NUTRITION
# -----------------------------------

elif page == "Diet & Nutrition":

    st.title("🥗 AI Diet & Nutrition Assistant")

    st.write(
        "Get general food and nutrition guidance."
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    goal = st.selectbox(
        "Your health goal",
        [
            "Healthy eating",
            "Weight management",
            "Muscle development",
            "Balanced nutrition",
            "Improve eating habits"
        ]
    )

    preference = st.selectbox(
        "Food preference",
        [
            "Vegetarian",
            "Non-vegetarian",
            "Both",
            "Vegan"
        ]
    )

    allergies = st.text_input(
        "Food allergies",
        placeholder="Example: peanuts, milk"
    )

    conditions = st.text_area(
        "Relevant medical conditions (optional)",
        placeholder="Example: diabetes, kidney disease, pregnancy"
    )

    if st.button("Generate My Diet Plan"):

        with st.spinner("Creating your diet plan..."):

            result = create_diet_plan(
                age,
                goal,
                preference,
                allergies,
                conditions,
                language
            )

        st.subheader("Your Diet Plan")
        st.write(result)

        st.warning(
            "This is general nutrition guidance, not a medical "
            "prescription. Consult a qualified dietitian for "
            "medical dietary requirements."
        )


# -----------------------------------
# HEALTH SUMMARY
# -----------------------------------

elif page == "Health Summary":

    st.title("📋 Health Summary Generator")

    st.write(
        "Paste your medical report information "
        "to generate a simple summary."
    )

    report = st.text_area(
        "Paste your report details",
        height=250
    )

    if st.button("Generate Health Summary"):

        if report.strip():

            with st.spinner("Generating summary..."):

                summary = create_summary(
                    report,
                    language
                )

            st.subheader("Your Health Summary")
            st.write(summary)

        else:

            st.warning(
                "Please enter your report information."
            )


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "💚 Sehat Saathi AI | Bilingual Healthcare Assistant | "
    "For educational purposes only."
)
