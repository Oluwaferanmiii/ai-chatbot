from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # load from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_bot_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Oops! Something went wrong: {e}"
