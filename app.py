
import streamlit as st
from PIL import Image
from io import BytesIO

from utils.report_tools import extract_pdf_text
from agents.medical_report_agent import analyze_report
from agents.medicine_agent import analyze_medicine, analyze_medicine_image
from agents.health_assistant_agent import health_chat
from agents.health_summary_agent import create_summary
from agents.diet_agent import create_diet_plan
from agents.safety_agent import check_emergency
from agents.voice_agent import transcribe_audio, speak_response


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sehat Saathi AI",
    page_icon="💚",
    layout="wide"
)


# ==========================================
# AUTOMATIC LIGHT / DARK THEME CSS
# ==========================================

st.markdown("""
<style>

/* Main application: follows selected Streamlit theme */
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Main content */
[data-testid="stAppViewContainer"] {
    background-color: var(--background-color);
    color: var(--text-color);
}

[data-testid="stAppViewContainer"] .main {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Headings and normal text */
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main li,
[data-testid="stAppViewContainer"] .main label {
    color: var(--text-color);
}

/* Main title */
.main-title {
    color: var(--primary-color) !important;
    font-size: 38px;
    font-weight: 800;
}

/* Subtitle */
.subtitle {
    color: var(--text-color) !important;
    opacity: 0.8;
    font-size: 16px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-color) !important;
}

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    color: var(--primary-color) !important;
    font-weight: 800;
}

/* Sidebar navigation */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label p,
[data-testid="stSidebar"] [role="radiogroup"] label span {
    color: var(--text-color) !important;
}

/* Input labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label,
.stFileUploader label {
    color: var(--text-color) !important;
    font-weight: 600;
}

/* Text input fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-testid="stChatInput"] textarea {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 8px;
}

/* Input placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-color) !important;
    opacity: 0.6;
}

/* Dropdown fields */
.stSelectbox [data-baseweb="select"] > div {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border-color: var(--primary-color) !important;
}

/* Dropdown menu */
[data-baseweb="popover"],
[data-baseweb="menu"] {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
}

[data-baseweb="menu"] li {
    color: var(--text-color) !important;
}

/* Buttons: retain Streamlit theme's accessible colors */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: var(--secondary-background-color);
    border: 1px dashed var(--primary-color);
    border-radius: 12px;
    padding: 10px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border: 1px solid var(--primary-color);
    border-radius: 14px;
}

/* Chat message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: var(--text-color);
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: var(--text-color);
    opacity: 0.2;
}

/* Links */
a {
    color: var(--primary-color) !important;
}

/* Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "report_result" not in st.session_state:
    st.session_state.report_result = ""


# ==========================================
# SIDEBAR
# ==========================================

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

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

    st.markdown(
        '<div class="main-title">💚 Sehat Saathi AI</div>',
        unsafe_allow_html=True
    )

    if language == "Urdu":
        st.subheader("آپ کا صحت کا ساتھی")
        st.write("اپنی صحت کے بارے میں آسان معلومات حاصل کریں۔")
    else:
        st.subheader("Your Intelligent Healthcare Companion")
        st.write(
            "Understand your health with AI-powered assistance."
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "**🩻 Medical Report Analysis**\n\n"
            "Upload medical reports and images "
            "to receive easy explanations."
        )

        st.success(
            "**💊 Medicine Scanner**\n\n"
            "Upload medicine packaging to examine "
            "visible medicine information."
        )

        st.info(
            "**🥗 Diet & Nutrition**\n\n"
            "Get general nutrition guidance "
            "with Pakistani food options."
        )

    with col2:

        st.success(
            "**💬 AI Health Chat**\n\n"
            "Ask general healthcare questions "
            "in English or Urdu."
        )

        st.info(
            "**📋 Health Summary**\n\n"
            "Turn medical report information "
            "into an easy-to-understand summary."
        )

        st.success(
            "**🎙️ Voice Assistant**\n\n"
            "Speak your questions and listen "
            "to AI-generated responses."
        )

    st.divider()

    st.warning(
        "Sehat Saathi AI provides educational health information. "
        "It does not replace doctors, radiologists, pharmacists "
        "or emergency medical services."
    )


# ==========================================
# MEDICAL REPORT ANALYSIS
# ==========================================

elif page == "Medical Report Analysis":

    st.title("🩻 Medical Report Analysis")

    st.write(
        "Upload a medical report, X-ray or medical image."
    )

    uploaded_file = st.file_uploader(
        "Upload your medical file",
        type=["png", "jpg", "jpeg", "webp", "pdf"],
        key="medical_upload"
    )

    if uploaded_file:

        file_bytes = uploaded_file.getvalue()

        is_pdf = uploaded_file.name.lower().endswith(".pdf")

        if is_pdf:

            with st.spinner("Reading your medical report..."):

                extracted_text = extract_pdf_text(file_bytes)

            st.subheader("Extracted Report Text")

            st.text_area(
                "Report content",
                extracted_text,
                height=200
            )

            if st.button("Analyze Medical Report"):

                with st.spinner("Analyzing your report..."):

                    result = analyze_report(
                        extracted_text,
                        language,
                        is_image=False
                    )

                    st.session_state.report_result = result

            if st.session_state.report_result:

                st.subheader("Medical Report Explanation")
                st.write(st.session_state.report_result)

        else:

            st.image(
                file_bytes,
                caption="Uploaded medical image",
                width=500
            )

            if st.button("Analyze Medical Image"):

                with st.spinner("Analyzing medical image..."):

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

            if st.session_state.report_result:

                st.subheader("Medical Image Explanation")
                st.write(st.session_state.report_result)

        if st.session_state.report_result:

            if st.button("Create Health Summary"):

                with st.spinner("Creating your summary..."):

                    summary = create_summary(
                        st.session_state.report_result,
                        language
                    )

                st.subheader("Health Summary")
                st.write(summary)

    st.caption(
        "Medical image analysis is experimental. "
        "A qualified radiologist must interpret X-rays."
    )


# ==========================================
# MEDICINE SCANNER
# ==========================================

elif page == "Medicine Scanner":

    st.title("💊 Medicine Information Scanner")

    st.write(
        "Upload a clear medicine package picture "
        "or enter the medicine name."
    )

    medicine_image = st.file_uploader(
        "Upload Medicine Picture",
        type=["png", "jpg", "jpeg", "webp"],
        key="medicine_upload"
    )

    medicine_name = st.text_input(
        "Or enter medicine name manually"
    )

    if medicine_image:

        st.image(
            medicine_image,
            caption="Uploaded medicine picture",
            width=350
        )

    if st.button("Identify Medicine"):

        if medicine_image:

            with st.spinner("Reading medicine packaging..."):

                image = Image.open(
                    BytesIO(medicine_image.getvalue())
                ).convert("RGB")

                buffer = BytesIO()

                image.save(
                    buffer,
                    format="JPEG",
                    quality=85
                )

                result = analyze_medicine_image(
                    buffer.getvalue(),
                    language
                )

            st.subheader("Medicine Information")
            st.write(result)

        elif medicine_name.strip():

            with st.spinner("Checking medicine information..."):

                result = analyze_medicine(
                    medicine_name,
                    language
                )

            st.subheader("Medicine Information")
            st.write(result)

        else:

            st.warning(
                "Please upload a medicine picture "
                "or enter a medicine name."
            )

    st.warning(
        "AI medicine identification can be incorrect. "
        "Always verify medicine details with a pharmacist. "
        "Do not change your medication based on AI output."
    )


# ==========================================
# AI HEALTH CHAT
# ==========================================

elif page == "AI Health Chat":

    st.title("💬 Sehat Saathi AI Health Assistant")

    st.write(
        "Ask general healthcare questions in English or Urdu."
    )

    # Display conversation history

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Voice input

    audio = st.audio_input(
        "🎙️ Record your health question"
    )

    if audio and st.button("Process Voice Message"):

        with st.spinner("Converting your voice to text..."):

            transcribed_text = transcribe_audio(
                audio.getvalue(),
                language
            )

        if transcribed_text and not transcribed_text.startswith(
            "Voice recognition error:"
        ) and not transcribed_text.startswith(
            "Groq API key is missing"
        ):

            st.session_state.voice_question = transcribed_text

        else:

            st.error(transcribed_text)

    # Text input

    question = st.chat_input(
        "Ask your health question..."
    )

    # Use transcribed voice if available

    voice_question = st.session_state.pop(
        "voice_question",
        None
    )

    if voice_question:
        question = voice_question
        st.write("Recognized speech:", question)

    if question:

        if check_emergency(question):

            if language == "Urdu":

                st.error(
                    "ممکنہ طبی ایمرجنسی۔ "
                    "فوراً مقامی ایمرجنسی سروس سے رابطہ کریں "
                    "یا قریبی ہسپتال جائیں۔"
                )

            else:

                st.error(
                    "Possible medical emergency. "
                    "Contact local emergency services "
                    "or go to the nearest emergency department immediately."
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

    # Speak the last assistant response

    if st.session_state.messages:

        last_message = st.session_state.messages[-1]

        if last_message["role"] == "assistant":

            if st.button("🔊 Speak Last Response"):

                with st.spinner("Generating speech..."):

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


# ==========================================
# DIET AND NUTRITION
# ==========================================

elif page == "Diet & Nutrition":

    st.title("🥗 AI Diet & Nutrition Assistant")

    st.write(
        "Get general nutrition guidance "
        "with practical Pakistani food options."
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
        placeholder="Example: diabetes, kidney disease"
    )

    if st.button("Generate My Diet Plan"):

        with st.spinner("Preparing your diet plan..."):

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
            "prescription. Consult a qualified dietitian "
            "for medical dietary requirements."
        )


# ==========================================
# HEALTH SUMMARY
# ==========================================

elif page == "Health Summary":

    st.title("📋 Health Summary Generator")

    st.write(
        "Paste your medical report information "
        "to generate a simple health summary."
    )

    report = st.text_area(
        "Paste your medical report details",
        height=250,
        placeholder="Paste your report text here..."
    )

    if st.button("Generate Health Summary"):

        if report.strip():

            with st.spinner("Generating your summary..."):

                summary = create_summary(
                    report,
                    language
                )

            st.subheader("Your Health Summary")
            st.write(summary)

        else:

            st.warning(
                "Please enter your medical report information."
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "💚 Sehat Saathi AI | Bilingual Healthcare Assistant"
)

st.caption(
    "For educational purposes only. "
    "Not a replacement for professional medical advice."
)
