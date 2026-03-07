from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_images(activity, images):
    """
    images = list of dicts from Pixabay
    """

    if not images:
        return None

    texts = []

    for img in images:
        tags = img.get("tags", "")
        texts.append(tags)

    # embed activity + tags
    embeddings = model.encode([activity] + texts)

    activity_vec = embeddings[0]
    image_vecs = embeddings[1:]

    scores = cosine_similarity([activity_vec], image_vecs)[0]

    best_index = scores.argmax()

    return images[best_index]["webformatURL"]
