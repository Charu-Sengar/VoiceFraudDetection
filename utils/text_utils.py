# utils/text_utils.py
import re

def clean_text(text: str) -> str:
    """
    Cleans and normalizes transcript text.
    Removes fillers, punctuation, and extra spaces.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # remove punctuation
    text = re.sub(r'\b(uh|um|hmm|haan|haina|ok|okay|please|thank)\b', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
