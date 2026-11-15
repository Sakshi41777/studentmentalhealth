import requests
import os
from dotenv import load_dotenv
from .image_ranker import rank_images

load_dotenv()

# Two free photo sources. Whichever key is set is used; Pexels first when both are set.
#   PEXELS_KEY   https://www.pexels.com/api/       (200 requests an hour)
#   PIXABAY_KEY  https://pixabay.com/api/docs/
PEXELS_KEY = os.getenv("PEXELS_KEY")
PEXELS_URL = "https://api.pexels.com/v1/search"

PIXABAY_KEY = os.getenv("PIXABAY_KEY")
PIXABAY_URL = "https://pixabay.com/api/"


def _from_pexels(activity):

    r = requests.get(
        PEXELS_URL,
        headers={"Authorization": PEXELS_KEY},
        params={"query": activity, "orientation": "landscape", "per_page": 15},
        timeout=10,
    )

    if r.status_code != 200:
        print("Pexels error:", r.status_code, r.text[:200])
        return None

    # Same shape the ranker already understands: words describing the photo + its link.
    hits = []
    for photo in r.json().get("photos", []):
        src = photo.get("src") or {}
        url = src.get("landscape") or src.get("large") or src.get("medium")
        if url:
            hits.append({"tags": photo.get("alt", ""), "webformatURL": url})

    return rank_images(activity, hits)


def _from_pixabay(activity):

    params = {
        "key": PIXABAY_KEY,
        "q": activity,
        "image_type": "photo",
        "orientation": "horizontal",
        "safesearch": "true",
        "per_page": 15
    }

    r = requests.get(PIXABAY_URL, params=params, timeout=10)

    if r.status_code != 200:
        print("Pixabay error:", r.text)
        return None

    hits = r.json().get("hits", [])

    # 🧠 AI RANKING
    return rank_images(activity, hits)


def fetch_image(activity):

    sources = (
        ("Pexels", PEXELS_KEY, _from_pexels),
        ("Pixabay", PIXABAY_KEY, _from_pixabay),
    )

    for name, key, search in sources:

        # No key for this source: skip it.
        if not key:
            continue

        # One failed photo lookup must not throw away the whole wellness report.
        try:
            url = search(activity)
            if url:
                return url
        except Exception as e:
            print(name, "request failed:", e)

    # Nothing found: the card falls back to one of the app's own pictures.
    return None
