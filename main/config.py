import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CROQ_API_KEY = os.getenv("CROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_CODE")
GEMINI_API_KEY = os.getenv("GEMINI_API_CODE")

