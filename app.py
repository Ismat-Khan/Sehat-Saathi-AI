
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
    layout="wide"
)


# ==========================================
# CSS - THEME, SIDEBAR AND RESPONSIVENESS
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

[data-testid="stMainBlockContainer"] {
    max-width: 100%;
}

/* MAIN HEADING */

.main-title {
    color: var(--primary-color) !important;
    font-size: 36px;
    font-weight: 800;
    line-height: 1.3;
}


/* ==========================================
   SIDEBAR - SOLID THEME-AWARE BACKGROUND
   ========================================== */

[data-testid="stSidebar"] {
    background-color: var(--background-color) !important;
    opacity: 1 !important;
    isolation: isolate;
    z-index: 1001 !important;
    backdrop-filter: none !important;
}

[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {
    background-color: var(--background-color) !important;
    opacity: 1 !important;
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

[data-testid="stSidebar"] h2 {
    color: var(--primary-color) !important;
    font-weight: 800;
}

/* Radio navigation spacing */

[data-testid="stSidebar"] [data-testid="stRadio"] {
    width: 100%;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;
    line-height: 1.5 !important;
    padding: 9px 5px !important;
    margin-bottom: 5px !important;
}

/* Sidebar select box */

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
}


/* ==========================================
   BUTTONS - CLEAR IN BOTH THEMES
   ========================================== */

/* Primary buttons only */

button[kind="primary"] {
    background-color: #315F9B !important;
    color: #FFFFFF !important;
    border: 1px solid #315F9B !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-height: 44px;
}

button[kind="primary"]:hover {
    background-color: #244A7D !important;
    color: #FFFFFF !important;
    border-color: #244A7D !important;
}

button[kind="primary"] p,
button[kind="primary"] span {
    color: #FFFFFF !important;
}


/* ==========================================
   HOME PAGE - PASTEL FEATURE CARDS
   ========================================== */

/* Medical Report - Blue */

.st-key-home_report_card {
    background-color: #EAF3FF !important;
    border: 1px solid #D4E5FC !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-height: 220px;
}

.st-key-home_report_card h3,
.st-key-home_report_card p {
    color: #315B91 !important;
}

/* Medicine Scanner - Green */

.st-key-home_medicine_card {
    background-color: #EAF8F0 !important;
    border: 1px solid #D0EEDD !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-height: 220px;
}

.st-key-home_medicine_card h3,
.st-key-home_medicine_card p {
    color: #286447 !important;
}

/* AI Chat - Purple */

.st-key-home_chat_card {
    background-color: #F2ECFF !important;
    border: 1px solid #E1D5FA !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-height: 220px;
}

.st-key-home_chat_card h3,
.st-key-home_chat_card p {
    color: #62458D !important;
}

/* Diet - Orange */

.st-key-home_diet_card {
    background-color: #FFF4E5 !important;
    border: 1px solid #F6E2C5 !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-height: 220px;
}

.st-key-home_diet_card h3,
.st-key-home_diet_card p {
    color: #85551F !important;
}

/* Health Summary - Teal */

.st-key-home_summary_card {
    background-color: #E8F7F8 !important;
    border: 1px solid #D0EBED !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-height: 220px;
}


/* ==========================================
   INPUT FIELDS
   ========================================== */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 10px;
    font-size: 16px !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
}

[data-testid="stFileUploader"] {
    background-color: var(--secondary-background-color);
    border: 1px dashed var(--primary-color);
    border-radius: 12px;
    padding: 10px;
}


/* ==========================================
   CHAT AND MEDIA
   ========================================== */

[data-testid="stChatMessage"] {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border: 1px solid var(--primary-color);
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stChatInput"] {
    width: 100%;
}

[data-testid="stImage"] img {
    max-width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 10px;
}

audio {
    max-width: 100%;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: var(--text-color);
    opacity: 0.2;
}

a {
    color: var(--primary-color) !important;
}

footer {
    visibility: hidden;
}


/* ==========================================
   TABLET AND MOBILE
   ========================================== */

@media screen and (max-width: 768px) {

    [data-testid="stMainBlockContainer"] {
        padding: 1rem !important;
        max-width: 100% !important;
    }

    .main-title {
        font-size: 27px !important;
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

    p, label, li {
        font-size: 15px;
        line-height: 1.6;
    }

    /* Solid mobile sidebar */

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        background-color: var(--background-color) !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] h2 {
        font-size: 22px !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        font-size: 14px !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 9px 5px !important;
        line-height: 1.5 !important;
    }

    /* Feature card spacing */

    .st-key-home_report_card,
    .st-key-home_medicine_card,
    .st-key-home_chat_card,
    .st-key-home_diet_card,
    .st-key-home_summary_card {
        padding: 12px !important;
        min-height: 200px;
        box-sizing: border-box !important;
    }

    audio {
        width: 100% !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        font-size: 16px !important;
        min-height: 44px;
    }
}


/* ==========================================
   SMALL PHONES - NEAT CARD STACKING
   ========================================== */

@media screen and (max-width: 480px) {

    [data-testid="stMainBlockContainer"] {
        padding: 0.75rem !important;
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

    /* Two-column grid becomes one column on narrow phones */

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 12px !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
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
    "spoken_message_index": None,
    "page_navigation": "Home"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# NAVIGATION FUNCTION
# ==========================================

def go_to_page(target):
    st.session_state.page_navigation = target


# ==========================================
# CHAT QUESTION HANDLER
# ==========================================

def submit_chat_question(question, language):

    question = question.strip()

    if not question:
        return

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
# SIDEBAR - ORIGINAL RADIO NAVIGATION
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
        key="page_navigation",
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
# HOME PAGE - TWO-COLUMN FEATURE GRID
# ==========================================

if page == "Home":

    st.markdown(
        '<div class="main-title">💚 Sehat Saathi AI</div>',
        unsafe_allow_html=True
    )

    st.subheader("Your Intelligent Healthcare Companion")

    st.write(
        "Understand your health with AI-powered assistance."
    )

    st.divider()

    st.markdown("### Explore Our Features")

    # FIRST ROW

    col1, col2 = st.columns(2, gap="medium")

    with col1:

        with st.container(
            border=True,
            key="home_report_card"
        ):

            st.markdown("### 🩻 Medical Report Analysis")

            st.write(
                "Upload medical reports and images for explanations."
            )

            st.button(
                "Open Medical Report Analysis →",
                key="home_report",
                type="primary",
                use_container_width=True,
                on_click=go_to_page,
                args=("Medical Report Analysis",)
            )

    with col2:

        with st.container(
            border=True,
            key="home_medicine_card"
        ):

            st.markdown("### 💊 Medicine Scanner")

            st.write(
                "Read visible information on medicine packaging."
            )

            st.button(
                "Open Medicine Scanner →",
                key="home_medicine",
                type="primary",
                use_container_width=True,
                on_click=go_to_page,
                args=("Medicine Scanner",)
            )

    # SECOND ROW

    col3, col4 = st.columns(2, gap="medium")

    with col3:

        with st.container(
            border=True,
            key="home_chat_card"
        ):

            st.markdown("### 💬 AI Health Chat")

            st.write(
                "Ask health questions in English or Urdu using text or voice."
            )

            st.button(
                "Open AI Health Chat →",
                key="home_chat",
                type="primary",
                use_container_width=True,
                on_click=go_to_page,
                args=("AI Health Chat",)
            )

    with col4:

        with st.container(
            border=True,
            key="home_diet_card"
        ):

            st.markdown("### 🥗 Diet & Nutrition")

            st.write(
                "Get general nutrition guidance with Pakistani food options."
            )

            st.button(
                "Open Diet & Nutrition →",
                key="home_diet",
                type="primary",
                use_container_width=True,
                on_click=go_to_page,
                args=("Diet & Nutrition",)
            )

    # THIRD ROW

    with st.container(
        border=True,
        key="home_summary_card"
    ):

        st.markdown("### 📋 Health Summary")

        st.write(
            "Generate easy-to-understand health summaries."
        )

        st.button(
            "Open Health Summary →",
            key="home_summary",
            type="primary",
            use_container_width=True,
            on_click=go_to_page,
            args=("Health Summary",)
        )

    st.divider()

    st.warning(
        "Sehat Saathi AI provides educational health information. "
        "It does not replace doctors or emergency medical services."
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
# AI HEALTH CHAT
# ==========================================

elif page == "AI Health Chat":

    st.title("💬 Sehat Saathi AI")

    st.caption(
        "Ask your health questions in English or Urdu."
    )

    for i, message in enumerate(st.session_state.messages):

        with st.chat_message(message["role"]):

            st.write(message["content"])

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

                if st.session_state.spoken_message_index == i:

                    if st.session_state.spoken_audio:

                        st.audio(
                            st.session_state.spoken_audio,
                            format="audio/mp3"
                        )

    prompt = st.chat_input(
        "Ask anything about your health...",
        accept_audio=True,
        audio_sample_rate=16000,
        key="health_chat_input"
    )

    if prompt:

        question = ""

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

        elif prompt.text:

            question = prompt.text.strip()

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
