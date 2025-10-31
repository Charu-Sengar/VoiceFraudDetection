# download_model.py
from faster_whisper import WhisperModel

# Correct usage: first argument is model_size_or_path
model = WhisperModel(
    "tiny",                # model_size_or_path
    device="cpu",
    compute_type="int8"
)

print("✅ Tiny model downloaded and ready!")
