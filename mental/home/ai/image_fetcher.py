import requests
import os
from dotenv import load_dotenv
from .image_ranker import rank_images

load_dotenv()

PIXABAY_KEY = os.getenv("PIXABAY_KEY")
PIXABAY_URL = "https://pixabay.com/api/"


def fetch_image(activity):

    # No key, no photo: the activity cards still show without an image.
    if not PIXABAY_KEY:
        return None

    params = {
        "key": PIXABAY_KEY,
        "q": activity,
        "image_type": "photo",
        "orientation": "horizontal",
        "safesearch": "true",
        "per_page": 15
    }

    # One failed photo lookup must not throw away the whole wellness report.
    try:
        r = requests.get(PIXABAY_URL, params=params, timeout=10)

        if r.status_code != 200:
            print("Pixabay error:", r.text)
            return None

        hits = r.json().get("hits", [])
    except Exception as e:
        print("Pixabay request failed:", e)
        return None

    # 🧠 AI RANKING
    best = rank_images(activity, hits)

    return best
