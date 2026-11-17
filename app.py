
import streamlit as st
from PIL import Image
from io import BytesIO

from tools.report_tools import extract_pdf_text

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
    layout="wide",
    initial_sidebar_state="auto"
)


# ==========================================
# RESPONSIVE DESIGN - LIGHT AND DARK MODE
# ==========================================

st.markdown("""
<style>

/* GENERAL APPLICATION */

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

[data-testid="stAppViewContainer"] {
    background-color: var(--background-color);
    color: var(--text-color);
}

[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main li,
[data-testid="stAppViewContainer"] .main label {
    color: var(--text-color);
}

.main-title {
    color: var(--primary-color) !important;
    font-size: 38px;
    font-weight: 800;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-color) !important;
}

[data-testid="stSidebar"] h2 {
    color: var(--primary-color) !important;
    font-weight: 800;
}

/* INPUTS */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 10px;
    font-size: 16px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: var(--text-color) !important;
    opacity: 0.65;
}

/* SELECT BOX */

.stSelectbox [data-baseweb="select"] > div {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border-color: var(--primary-color) !important;
}

/* BUTTONS */

div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 42px;
    transition: all 0.2s ease;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background-color: var(--secondary-background-color);
    border: 1px dashed var(--primary-color);
    border-radius: 12px;
    padding: 10px;
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border: 1px solid var(--primary-color);
    border-radius: 14px;
    padding: 12px;
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    width: 100%;
}

/* IMAGES */

[data-testid="stImage"] img {
    max-width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 10px;
}

/* ALERTS */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* DIVIDERS */

hr {
    border-color: var(--text-color);
    opacity: 0.2;
}

/* LINKS */

a {
    color: var(--primary-color) !important;
}

/* AUDIO PLAYER */

audio {
    max-width: 100%;
}

/* HIDE FOOTER */

footer {
    visibility: hidden;
}


/* ==========================================
   TABLET AND MOBILE RESPONSIVENESS
   ========================================== */

@media screen and (max-width: 768px) {

    /* MAIN CONTENT AREA */

    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
        max-width: 100% !important;
    }

    /* HEADINGS */

    .main-title {
        font-size: 27px !important;
        line-height: 1.3 !important;
    }

    h1 {
        font-size: 26px !important;
        line-height: 1.3 !important;
    }

    h2 {
        font-size: 22px !important;
    }

    h3 {
        font-size: 19px !important;
    }

    /* TEXT */

    p, label, li {
        font-size: 15px;
        line-height: 1.6;
    }

    /* STACK COLUMNS */

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.7rem !important;
    }

    [data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* BUTTONS */

    div.stButton > button {
        width: 100% !important;
        min-height: 44px;
        font-size: 15px !important;
    }

    /* INPUTS */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        font-size: 16px !important;
        min-height: 44px;
    }

    /* FILE UPLOADER */

    [data-testid="stFileUploader"] {
        width: 100% !important;
        padding: 8px !important;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        min-width: 0 !important;
        max-width: 85vw !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }

    [data-testid="stSidebar"] h2 {
        font-size: 22px !important;
        margin-bottom: 2px !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        font-size: 14px !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding-top: 5px !important;
        padding-bottom: 5px !important;
    }

    /* CHAT MESSAGES */

    [data-testid="stChatMessage"] {
        padding: 9px !important;
        border-radius: 12px !important;
    }

    /* CHAT INPUT */

    [data-testid="stChatInput"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* AUDIO */

    audio {
        width: 100% !important;
        max-width: 100% !important;
    }

    /* PREVENT HORIZONTAL SCROLLING */

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

}


/* ==========================================
   SMALL MOBILE PHONES
   ========================================== */

@media screen and (max-width: 480px) {

    [data-testid="stMainBlockContainer"] {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .main-title {
        font-size: 24px !important;
    }

    h1 {
        font-size: 23px !important;
    }

    h2 {
        font-size: 20px !important;
    }

    [data-testid="stSidebar"] {
        max-width: 88vw !important;
    }

    [data-testid="stChatMessage"] {
        padding: 8px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "messages": [],
    "language": "English",
    "report_result": "",
    "spoken_audio": None,
    "spoken_message_index": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# CHAT QUESTION HANDLER
# ==========================================

def submit_chat_question(question, language):

    question = question.strip()

    if not question:
        return

    # Basic emergency keyword check
    if check_emergency(question):

        if language == "Urdu":

            emergency_message = (
                "ممکنہ طبی ایمرجنسی۔ فوراً مقامی ایمرجنسی سروس "
                "سے رابطہ کریں یا قریبی ہسپتال کے ایمرجنسی ڈیپارٹمنٹ جائیں۔"
            )

        else:

            emergency_message = (
                "Possible medical emergency. Contact local emergency "
                "services or go to the nearest emergency department "
                "immediately. Do not wait for an AI response."
            )

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": emergency_message
        })

        return

    previous_messages = st.session_state.messages.copy()

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.spinner("Sehat Saathi AI is preparing your answer..."):

        answer = health_chat(
            question,
            previous_messages,
            language
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ==========================================
# SIDEBAR — RESPONSIVE NAVIGATION
# ==========================================

with st.sidebar:

    st.markdown(
        "<h2>💚 Sehat Saathi AI</h2>",
        unsafe_allow_html=True
    )

    st.caption("Your Intelligent Healthcare Companion")

    st.divider()

    language = st.selectbox(
        "🌐 Language / زبان",
        ["English", "Urdu"],
        index=0 if st.session_state.language == "English" else 1
    )

    st.session_state.language = language

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Choose a section",
        [
            "Home",
            "Medical Report Analysis",
            "Medicine Scanner",
            "AI Health Chat",
            "Diet & Nutrition",
            "Health Summary"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("Powered by Groq AI")

    if st.button(
        "Clear Chat History",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.spoken_audio = None
        st.session_state.spoken_message_index = None

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

        st.write(
            "اپنی صحت کے بارے میں آسان معلومات حاصل کریں۔"
        )

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
            "Upload medical reports and images for explanations."
        )

        st.success(
            "**💊 Medicine Scanner**\n\n"
            "Read visible information on medicine packaging."
        )

        st.info(
            "**🥗 Diet & Nutrition**\n\n"
            "Get general nutrition guidance with Pakistani food options."
        )

    with col2:

        st.success(
            "**💬 AI Health Chat**\n\n"
            "Ask healthcare questions in English or Urdu."
        )

        st.info(
            "**📋 Health Summary**\n\n"
            "Create easy-to-understand health summaries."
        )

        st.success(
            "**🎙️ Voice Assistant**\n\n"
            "Ask questions by voice and listen to responses."
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

                    st.session_state.report_result = analyze_report(
                        extracted_text,
                        language,
                        is_image=False
                    )

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

                    st.session_state.report_result = analyze_report(
                        buffer.getvalue(),
                        language,
                        is_image=True
                    )

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
                "Please upload a medicine picture or enter a medicine name."
            )

    st.warning(
        "AI medicine identification can be incorrect. "
        "Always verify medicine details with a pharmacist. "
        "Do not change medication based on AI output."
    )


# ==========================================
# AI HEALTH CHAT — BUILT-IN MICROPHONE
# ==========================================

elif page == "AI Health Chat":

    st.title("💬 Sehat Saathi AI")

    st.caption(
        "Ask your health questions in English or Urdu."
    )

    # DISPLAY CHAT HISTORY

    for i, message in enumerate(st.session_state.messages):

        with st.chat_message(message["role"]):

            st.write(message["content"])

            # READ ALOUD FEATURE

            if message["role"] == "assistant":

                if st.button(
                    "🔊 Read aloud",
                    key=f"read_aloud_{i}"
                ):

                    with st.spinner("Preparing voice..."):

                        audio_bytes = speak_response(
                            message["content"],
                            language
                        )

                    if audio_bytes:

                        st.session_state.spoken_audio = audio_bytes
                        st.session_state.spoken_message_index = i

                    else:

                        st.error("Voice generation failed.")

                # DISPLAY GENERATED AUDIO

                if st.session_state.spoken_message_index == i:

                    if st.session_state.spoken_audio:

                        st.audio(
                            st.session_state.spoken_audio,
                            format="audio/mp3"
                        )

    # INTEGRATED TEXT AND MICROPHONE INPUT

    prompt = st.chat_input(
        "Ask anything about your health...",
        accept_audio=True,
        audio_sample_rate=16000,
        key="health_chat_input"
    )

    # PROCESS USER INPUT

    if prompt:

        question = ""

        # VOICE INPUT

        if prompt.audio:

            with st.spinner("Converting your voice into text..."):

                question = transcribe_audio(
                    prompt.audio.getvalue(),
                    language
                )

            if (
                not question
                or question.startswith("Voice recognition error:")
                or question.startswith("Groq API key is missing")
            ):

                st.error(
                    question or "Could not recognize your voice."
                )

                st.stop()

            st.caption("🎙️ Voice transcription: " + question)

        # TEXT INPUT

        elif prompt.text:

            question = prompt.text.strip()

        # SEND TO AI

        if question:

            submit_chat_question(
                question,
                language
            )

            st.session_state.spoken_audio = None
            st.session_state.spoken_message_index = None

            st.rerun()


# ==========================================
# DIET AND NUTRITION
# ==========================================

elif page == "Diet & Nutrition":

    st.title("🥗 AI Diet & Nutrition Assistant")

    st.write(
        "Get general nutrition guidance with practical Pakistani food options."
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
            "This is general nutrition guidance, not a medical prescription. "
            "Consult a qualified dietitian for medical dietary requirements."
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
