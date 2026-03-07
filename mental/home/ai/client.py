from decouple import config
from groq import Groq

def get_ai_client():

    return Groq(api_key=config("GROQ_API_KEY"))
