# llm_client.py
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompt_templates import DETECT_PROMPT

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment")

client = OpenAI(api_key=api_key)

def analyze_with_llm(transcript: str) -> dict:
    prompt = DETECT_PROMPT.format(transcript=transcript)
    try:
        # Call OpenAI Chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        # Convert response to dictionary
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {
            "label": "Unknown",
            "confidence": 0.0,
            "reason": content[:200] if 'content' in locals() else "Failed to parse LLM response"
        }
    except Exception as e:
        # Log error for debugging
        print(f"[LLM ERROR] {str(e)}")
        result = {
            "label": "Unknown",
            "confidence": 0.0,
            "reason": f"Error during LLM call: {str(e)}"
        }
    return result
