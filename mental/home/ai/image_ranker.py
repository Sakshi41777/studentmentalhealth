"""
Picks the Pixabay photo whose tags best match an activity.

Default: a light keyword match that needs no ML libraries, so the app fits on a small
(512 MB) server. The original embedding-based ranking is still here: install
requirements-ml.txt and set SEMANTIC_RANKER=1 to use it (it needs about 1 GB of RAM).
"""
import os
import re

_STOP = {"the", "and", "for", "with", "person", "people", "wellness", "activity"}
_model = None


def _stem(word):
    for suffix in ("ing", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def _words(text):
    found = re.findall(r"[a-z]+", (text or "").lower())
    return {_stem(w) for w in found if len(w) > 2 and w not in _STOP}


def _keyword_best(activity, images):
    """Cosine similarity between the two sets of words. Ties keep Pixabay's own order."""
    wanted = _words(activity)
    best, best_score = images[0], -1.0
    for img in images:
        tags = _words(img.get("tags", ""))
        score = 0.0
        if wanted and tags:
            score = len(wanted & tags) / ((len(wanted) * len(tags)) ** 0.5)
        if score > best_score:
            best, best_score = img, score
    return best


def _semantic_best(activity, images):
    global _model
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")  # loaded on first use, not at import
    embeddings = _model.encode([activity] + [img.get("tags", "") for img in images])
    scores = cosine_similarity([embeddings[0]], embeddings[1:])[0]
    return images[int(scores.argmax())]


def rank_images(activity, images):
    """
    images = list of dicts from Pixabay
    """

    if not images:
        return None

    if os.getenv("SEMANTIC_RANKER") == "1":
        try:
            return _semantic_best(activity, images).get("webformatURL")
        except Exception as e:
            print("Semantic ranker unavailable, using keyword ranking:", e)

    return _keyword_best(activity, images).get("webformatURL")
