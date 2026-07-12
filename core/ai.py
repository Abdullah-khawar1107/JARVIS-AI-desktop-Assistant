import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Store conversation history
chat = model.start_chat(history=[])


def ask_ai(prompt):
    try:
        response = chat.send_message(prompt)
        return response.text

    except Exception as e:
        return "Error: " + str(e)


def reset_chat():
    global chat
    chat = model.start_chat(history=[])