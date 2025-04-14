import os
import requests
from dotenv import load_dotenv

load_dotenv()


def ask_bot_huggingface(message):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    HF_TOKEN = os.getenv("HF_API_TOKEN")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": f" {message}",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].replace(message, "").strip()
        elif isinstance(result, dict) and "error" in result:
            return f"Oops! HF API error: {result['error']}"
        else:
            return "Hmm... the response was a bit confusing 😅"

    except Exception as e:
        return f"Oops! Something went wrong: {e}"
