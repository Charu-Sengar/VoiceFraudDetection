# utils/audio_utils.py
import streamlit as st
from faster_whisper import WhisperModel

MODEL_SIZE = "small"  # tiny, base, small, medium, large-v2

# Load Whisper model once and cache it
@st.cache_resource(show_spinner=False)
def get_model():
    return WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")  # CPU-friendly

MODEL = get_model()

def audio_to_text(audio_path: str, beam_size: int = 3) -> str:
    """
    Transcribe audio file to text using cached faster-whisper model.
    """
    try:
        segments, _ = MODEL.transcribe(audio_path, beam_size=beam_size)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    except Exception as e:
        st.error(f"❌ Transcription error: {e}")
        return "Transcription failed."
