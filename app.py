import logging
from utils.audio_utils import audio_to_text
from utils.text_utils import clean_text
from llm_client import analyze_with_llm
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# --- Logging Setup ---
LOG_FILE = "data/processing.log"
os.makedirs("data", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

AUDIO_DIR = "data/raw_audio"
OUTPUT_FILE = "data/results.csv"
NUM_THREADS = 4  # Adjust based on your CPU cores


def process_file(file):
    path = os.path.join(AUDIO_DIR, file)
    try:
        logging.info(f"Started processing file: {file}")

        # Step 1: Convert audio → text
        text = audio_to_text(path, model_name="tiny")
        logging.info(f"Audio to text conversion successful for: {file}")

        # Step 2: Clean the text
        cleaned = clean_text(text)
        logging.info(f"Text cleaning completed for: {file}")

        # Step 3: Analyze with LLM
        result = analyze_with_llm(cleaned)
        logging.info(f"LLM analysis completed for: {file}")

        return {
            "audio_file": file,
            "transcript": cleaned,
            "label": result.get("label", ""),
            "confidence": result.get("confidence", ""),
            "reason": result.get("reason", "")
        }

    except Exception as e:
        logging.error(f"Error processing {file}: {e}")
        return {
            "audio_file": file,
            "transcript": "",
            "label": "Error",
            "confidence": 0.0,
            "reason": str(e)
        }


def main():
    logging.info("=== Starting Audio Processing Pipeline ===")

    if not os.path.exists(AUDIO_DIR):
        logging.warning(f"Audio directory '{AUDIO_DIR}' not found. Creating one.")
        os.makedirs(AUDIO_DIR, exist_ok=True)

    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith((".wav", ".flac", ".mp3"))]
    logging.info(f"Total files found: {len(audio_files)}")

    results = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = {executor.submit(process_file, f): f for f in audio_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing audio"):
            results.append(future.result())

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"All results saved to: {OUTPUT_FILE}")
    logging.info("=== Audio Processing Completed Successfully ===")

    print(f"\n📊 All results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
