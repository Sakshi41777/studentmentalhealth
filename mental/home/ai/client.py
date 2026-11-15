from decouple import config
from groq import Groq

# Groq retires models from time to time. Set GROQ_MODEL to change it without touching code.
MODEL = config("GROQ_MODEL", default="llama-3.3-70b-versatile")


def get_ai_client():

    return Groq(api_key=config("GROQ_API_KEY"))
