
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
# AUTOMATIC LIGHT / DARK THEME
# ==========================================

st.markdown("""
<style>
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

.subtitle {
    color: var(--text-color) !important;
    opacity: 0.8;
    font-size: 16px;
}

/* Sidebar */
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

[data-testid="stSidebar"] h1 {
    color: var(--primary-color) !important;
    font-weight: 800;
}

/* Inputs */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label,
.stFileUploader label {
    color: var(--text-color) !important;
    font-weight: 600;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
[data-testid="stChatInput"] textarea {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 8px;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-color) !important;
    opacity: 0.6;
}

/* Dropdown */
.stSelectbox [data-baseweb="select"] > div {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border-color: var(--primary-color) !important;
}

/* Buttons */
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

footer {
    visibility: hidden;
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
    "pending_voice_question": "",
    "voice_widget_version": 0,
    "spoken_audio": None
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

        st.session_state.spoken_audio = None
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

    st.session_state.spoken_audio = None


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
        st.session_state.pending_voice_question = ""
        st.session_state.spoken_audio = None
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
        st.write("Understand your health with AI-powered assistance.")

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

    st.write("Upload a medical report, X-ray or medical image.")

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
        "Always verify medicine details with a pharmacist."
    )


# ==========================================
# AI HEALTH CHAT AND VOICE ASSISTANT
# ==========================================

elif page == "AI Health Chat":

    st.title("💬 Sehat Saathi AI Health Assistant")

    st.write(
        "Ask your health questions by typing or recording your voice."
    )

    # --------------------------------------
    # SHOW CHAT HISTORY
    # --------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    st.divider()

    # --------------------------------------
    # VOICE QUESTION SECTION
    # --------------------------------------

    st.subheader("🎙️ Ask using your voice")

    st.write(
        "Record your question, review the converted text, "
        "and then send it to Sehat Saathi AI."
    )

    audio = st.audio_input(
        "Record your health question",
        key=f"voice_recording_{st.session_state.voice_widget_version}"
    )

    if audio:

        st.audio(
            audio,
            format="audio/wav"
        )

        if st.button(
            "Convert Voice to Text",
            use_container_width=True
        ):

            with st.spinner("Listening to your recording..."):

                transcription = transcribe_audio(
                    audio.getvalue(),
                    language
                )

            if (
                transcription
                and not transcription.startswith("Voice recognition error:")
                and not transcription.startswith("Groq API key is missing")
            ):

                st.session_state.pending_voice_question = transcription

            else:

                st.error(transcription)

    # --------------------------------------
    # REVIEW TRANSCRIPTION
    # --------------------------------------

    if st.session_state.pending_voice_question:

        st.success("Your voice has been converted into text.")

        edited_question = st.text_area(
            "Review or edit your question before sending:",
            value=st.session_state.pending_voice_question,
            key="voice_transcription_review",
            height=100
        )

        col_send, col_cancel = st.columns(2)

        with col_send:

            if st.button(
                "Send Question to AI",
                use_container_width=True
            ):

                if edited_question.strip():

                    st.session_state.pending_voice_question = ""

                    submit_chat_question(
                        edited_question,
                        language
                    )

                    st.session_state.voice_widget_version += 1

                    st.rerun()

        with col_cancel:

            if st.button(
                "Cancel Recording",
                use_container_width=True
            ):

                st.session_state.pending_voice_question = ""
                st.session_state.voice_widget_version += 1
                st.rerun()

    st.divider()

    # --------------------------------------
    # TEXT QUESTION SECTION
    # --------------------------------------

    st.subheader("⌨️ Or type your question")

    typed_question = st.chat_input(
        "Write your health question here..."
    )

    if typed_question:

        submit_chat_question(
            typed_question,
            language
        )

        st.rerun()

    # --------------------------------------
    # LISTEN TO LAST AI RESPONSE
    # --------------------------------------

    if st.session_state.messages:

        last_message = st.session_state.messages[-1]

        if last_message["role"] == "assistant":

            st.divider()

            st.subheader("🔊 Listen to AI Response")

            st.write(
                "Listen to the latest answer in your selected language."
            )

            if st.button(
                "Generate Voice Response",
                use_container_width=True
            ):

                with st.spinner("Preparing natural speech..."):

                    st.session_state.spoken_audio = speak_response(
                        last_message["content"],
                        language
                    )

            if st.session_state.spoken_audio:

                st.audio(
                    st.session_state.spoken_audio,
                    format="audio/mp3"
                )

            elif st.session_state.spoken_audio is None:

                st.caption(
                    "Select Generate Voice Response to listen to the answer."
                )

    st.caption(
        "If recording fails, allow microphone access in your browser "
        "and try again. You can always type your question instead."
    )


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
