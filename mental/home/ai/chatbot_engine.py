from .client import MODEL, get_ai_client, reasoning_options

SYSTEM_PROMPT = """
You are MindCare — a gentle mental wellness assistant.

RULES:
- Keep replies SHORT (2–3 lines max)
- Never write long paragraphs
- Always sound warm and friendly
- Use emojis occasionally 🙂
- Focus on emotions, not facts
- Redirect off-topic questions back to feelings
- Avoid theory
- Avoid politics
- Avoid general knowledge

Example style:

"I'm here with you 💛  
How are you feeling right now?"

Use comforting language.
"""

def chat_with_user(message):

    # A missing key or an API hiccup should give a kind reply, not a server error.
    try:
        client = get_ai_client()

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.4,
            # Room for the model's own thinking plus a 2-3 line reply (the prompt keeps it short).
            max_tokens=400,
            extra_body=reasoning_options()
        )

        reply = (response.choices[0].message.content or "").strip()

        if not reply:
            raise Exception("Empty reply from the model")

        return reply

    except Exception as e:
        print("Chatbot error:", e)
        return "I'm having trouble replying right now. Please try again in a moment."
