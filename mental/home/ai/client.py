from decouple import config
from groq import Groq

# Groq changes which models an account can use (llama-3.3-70b-versatile became
# enterprise-only). Set GROQ_MODEL to switch models without touching code.
MODEL = config("GROQ_MODEL", default="openai/gpt-oss-120b")


def get_ai_client():

    return Groq(api_key=config("GROQ_API_KEY"))


def reasoning_options():
    """
    GPT-OSS models "think" before they answer, and that thinking is counted in max_tokens.
    Ask for short thinking and keep it out of the reply. Other models reject these
    options, so they are only sent to GPT-OSS models.
    """
    if "gpt-oss" in MODEL:
        return {"reasoning_effort": "low", "include_reasoning": False}
    return None
