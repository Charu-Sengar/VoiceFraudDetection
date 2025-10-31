# app_ui.py
import warnings
warnings.filterwarnings("ignore", message="Examining the path of torch.classes raised")

import streamlit as st
from faster_whisper import WhisperModel
from llm_client import analyze_with_llm
import os

# ----------------------------
# Model setup
# ----------------------------
MODEL_NAME = "tiny"       # Hugging Face model name
DEVICE = "cpu"            # CPU for Docker
COMPUTE_TYPE = "float32"  # Safe for CPU

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        model = WhisperModel(MODEL_NAME, device=DEVICE, compute_type=COMPUTE_TYPE)
        return model
    except Exception as e:
        st.error(f"Failed to load Whisper model: {e}")
        return None

MODEL = load_model()

# ----------------------------
# Audio transcription
# ----------------------------
def audio_to_text(audio_path: str) -> str:
    if MODEL is None:
        return "Whisper model not loaded."
    try:
        segments, _ = MODEL.transcribe(audio_path)
        return " ".join([segment.text for segment in segments]).strip()
    except Exception as e:
        return f"Error during transcription: {str(e)}"

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("📞 Voice Fraud Detection")
st.write("Upload an audio file or paste a transcript to check if it's fraud or genuine.")

tab_audio, tab_text = st.tabs(["🎧 Upload Audio", "📝 Paste Transcript"])

# -------- Audio Upload Tab --------
with tab_audio:
    uploaded_file = st.file_uploader("Upload audio (wav, mp3, flac)", type=["wav", "mp3", "flac"])
    if uploaded_file:
        os.makedirs("temp_audio", exist_ok=True)
        temp_path = os.path.join("temp_audio", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("🎧 Transcribing audio..."):
            transcript = audio_to_text(temp_path)

        try: os.remove(temp_path)
        except: pass

        st.subheader("Transcript")
        st.text_area("📄", transcript, height=200)

        if "Error during transcription" not in transcript:
            with st.spinner("🤖 Analyzing for fraud..."):
                try:
                    result = analyze_with_llm(transcript)
                except Exception as e:
                    result = {"label": "Error", "reason": str(e), "confidence": 0.0}
            st.subheader("Analysis Result")
            st.json(result)

# -------- Text Input Tab --------
with tab_text:
    user_text = st.text_area("Paste transcript here", height=200)
    if st.button("Analyze Text") and user_text.strip() != "":
        with st.spinner("🤖 Analyzing for fraud..."):
            try:
                result = analyze_with_llm(user_text.strip())
            except Exception as e:
                result = {"label": "Error", "reason": str(e), "confidence": 0.0}
        st.subheader("Analysis Result")
        st.json(result)
