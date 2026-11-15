import json
import re
from .client import MODEL, get_ai_client, reasoning_options
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


# 🖼️ The app's own pictures, used when no photo is found or a photo fails to load.
FALLBACK_IMAGES = [
    (("breath", "meditat", "mindful", "ground", "calm"), "/static/images/breathing.jpg"),
    (("yoga", "stretch", "muscle", "relax"), "/static/images/yoga.jpg"),
    (("sleep", "rest", "sunset", "screen", "night", "bed"), "/static/images/sleep.jpg"),
    (("walk", "nature", "exercise", "move", "outdoor", "run"), "/static/images/physical1.jpg"),
]


def fallback_image(title, index):
    lowered = title.lower()
    for words, path in FALLBACK_IMAGES:
        if any(w in lowered for w in words):
            return path
    return FALLBACK_IMAGES[index % len(FALLBACK_IMAGES)][1]


def photo_query(act):
    """Search words for an activity's photo: the curated map, else the model's own words, else the title."""
    title = act.get("title", "")
    if title in ACTIVITY_QUERY_MAP:
        return ACTIVITY_QUERY_MAP[title]
    suggested = re.sub(r"[^A-Za-z ]", " ", str(act.get("image_query", ""))).strip()
    if suggested:
        return " ".join(suggested.split()[:6])
    # Titles like "Guided Breathing (5 min)" search badly: drop brackets and numbers.
    plain = re.sub(r"\(.*?\)|[^A-Za-z ]", " ", title)
    return " ".join(plain.split()) + " calm person"


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
      "desc": "...",
      "image_query": "2 to 4 plain words describing a calm stock photo for this activity"
    }}
  ]
}}

Return EXACTLY 6 activities.
"""

    try:
        client = get_ai_client()

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=2000,
            extra_body=reasoning_options()
        )

        raw = response.choices[0].message.content or ""
        print("RAW LLM RESPONSE:\n", raw)

        parsed = extract_json(raw)

        if parsed and "activities" in parsed:

            for index, act in enumerate(parsed["activities"]):

                title = act.get("title", "")

                img = fetch_image(photo_query(act))

                # The template swaps to fallback_image if the photo cannot be loaded.
                act["fallback_image"] = fallback_image(title, index)
                act["image_url"] = img or act["fallback_image"]

            return parsed

        raise Exception("Invalid LLM JSON")

    except Exception as e:
        print("LLM wellness error:", e)

        return {
            "summary": "Please take gentle care of yourself.",
            "activities": []
        }
