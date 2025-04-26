# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()


# def ask_bot_huggingface(message):
#     API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
#     HF_TOKEN = os.getenv("HF_API_TOKEN")

#     headers = {
#         "Authorization": f"Bearer {HF_TOKEN}"
#     }

#     payload = {
#         "inputs": f" {message}",
#         "parameters": {
#             "max_new_tokens": 200,
#             "temperature": 0.7,
#         }
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
#         result = response.json()

#         if isinstance(result, list) and "generated_text" in result[0]:
#             return result[0]["generated_text"].replace(message, "").strip()
#         elif isinstance(result, dict) and "error" in result:
#             return f"Oops! HF API error: {result['error']}"
#         else:
#             return "Hmm... the response was a bit confusing 😅"

#     except Exception as e:
#         return f"Oops! Something went wrong: {e}"


import random


def ask_bot_huggingface(message):
    sample_replies = [
        "Hello! How can I help you today?",
        "I'm just a simple bot, but I'm here for you!",
        "Could you please tell me more?",
        "That's interesting! Tell me more.",
        "I'm still learning, but I think you're awesome!",
        "Hmm... that's a good question! Let me think...",
        "Sure! I'm always ready to chat with you!",
    ]
    return random.choice(sample_replies)
