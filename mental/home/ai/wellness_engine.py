import json
import re
from .client import get_ai_client
from .image_fetcher import fetch_image


def extract_json(text):
    try:
        text = text.strip()
        text = re.sub(r"^```json", "", text)
        text = re.sub(r"```$", "", text)

        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group()) if match else json.loads(text)

    except Exception as e:
        print("JSON extraction error:", e)
        return None


# 🔥 ACTIVITY → REAL PHOTO QUERY MAP
ACTIVITY_QUERY_MAP = {

    "Deep Breathing Exercises": "person breathing fresh air morning balcony",

    "Nature Walks": "person walking forest path sunlight",

    "Journaling": "hand writing journal notebook wooden desk",

    "Mindfulness Meditation": "person sitting meditation park calm",

    "Creative Expression": "painting art supplies colorful table",

    "Grounding Techniques": "bare feet grass nature mindfulness",

    "Progressive Muscle Relaxation": "person lying yoga mat relaxing",

    "Self-Care Routine": "woman relaxing spa towel candle",

    "Gratitude Journaling": "open journal gratitude pen coffee",

    "Yoga Practice": "person doing yoga outdoor sunrise",

    "Social Connection": "friends talking smiling outdoors"
}


def generate_wellness_report(level, stress, anxiety, depression):

    severity_map = {
        0: "stable",
        1: "moderate emotional strain",
        2: "elevated stress"
    }

    prompt = f"""
You are a compassionate mental wellness assistant.

User scores:
Stress: {stress}%
Anxiety: {anxiety}%
Depression: {depression}%
Overall condition: {severity_map.get(level)}

IMPORTANT RULES:
- Do NOT give medical diagnosis
- Be supportive, calm, and brief
- Keep summary to 1–2 short sentences (max 30 words total)
- Avoid fluffy language

Return STRICT JSON ONLY:

{{
  "summary": "1–2 short sentences",
  "activities": [
    {{
      "title": "...",
      "desc": "..."
    }}
  ]
}}

Return EXACTLY 6 activities.
"""

    try:
        client = get_ai_client()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=1200
        )

        raw = response.choices[0].message.content
        print("RAW LLM RESPONSE:\n", raw)

        parsed = extract_json(raw)

        if parsed and "activities" in parsed:

            for act in parsed["activities"]:

                title = act["title"]

                # ✅ Use mapped query if exists
                search_query = ACTIVITY_QUERY_MAP.get(
                    title,
                    f"{title} wellness activity person"
                )

                img = fetch_image(search_query)
                act["image_url"] = img or ""

            return parsed

        raise Exception("Invalid LLM JSON")

    except Exception as e:
        print("LLM wellness error:", e)

        return {
            "summary": "Please take gentle care of yourself.",
            "activities": []
        }
