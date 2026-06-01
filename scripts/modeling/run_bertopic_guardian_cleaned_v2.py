from pathlib import Path
import re

import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS


# =========================
# 1. Set paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "datasets" / "theguardian" / "guardian_cleaned.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "member3"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 2. Load cleaned data
# =========================

print("Loading Guardian cleaned data...")

df = pd.read_json(DATA_PATH, lines=True)

print("Columns:", df.columns.tolist())
print("Number of rows before filtering:", len(df))

# Use cleaned text from Member 2 preprocessing
df = df.dropna(subset=["clean_text"])
df["clean_text"] = df["clean_text"].astype(str)

# Remove very short texts
df = df[df["clean_text_length"] > 20]

CUSTOM_STOPWORDS = {
    "said", "say", "says", "new", "year", "years", "time", "people",
    "like", "just", "make", "want", "need", "going", "think", "know",
    "told", "according", "reported", "guardian", "gmt", "bst",
    "uk", "us", "australia", "australian",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "2020", "2021", "2022", "2023"
}

def light_clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["model_text"] = df["clean_text"].apply(light_clean)
df = df[df["model_text"].str.len() > 50]

documents = df["model_text"].tolist()

print("Number of documents used:", len(documents))


# =========================
# 3. Configure BERTopic
# Paper Table 2 Guardian best parameters:
# n_gram=2, n_clusters=2,
# n_components=5, n_neighbors=20
# =========================

print("Configuring BERTopic model...")

stop_words = list(ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS))

vectorizer_model = CountVectorizer(
    ngram_range=(1, 2),
    stop_words=stop_words,
    min_df=2,
)

umap_model = UMAP(
    n_neighbors=20,
    n_components=5,
    random_state=42
)

cluster_model = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

topic_model = BERTopic(
    vectorizer_model=vectorizer_model,
    umap_model=umap_model,
    hdbscan_model=cluster_model,
    calculate_probabilities=False,
    verbose=True
)


# =========================
# 4. Fit model
# =========================

print("Training BERTopic model...")

topics, probs = topic_model.fit_transform(documents)


# =========================
# 5. Save outputs
# =========================

print("Saving outputs...")

topic_info = topic_model.get_topic_info()
topic_info.to_csv(OUTPUT_DIR / "guardian_bertopic_v2_topic_info.csv", index=False)

topic_words = []

for topic_id in topic_info["Topic"]:
    if topic_id == -1:
        continue

    words = topic_model.get_topic(topic_id)

    if words is None:
        continue

    for word, score in words:
        topic_words.append({
            "topic": topic_id,
            "word": word,
            "score": score
        })

topic_words_df = pd.DataFrame(topic_words)
topic_words_df.to_csv(OUTPUT_DIR / "guardian_bertopic_v2_topic_words.csv", index=False)

doc_topics = df[["title", "section", "date", "url"]].copy()
doc_topics["topic"] = topics
doc_topics.to_csv(OUTPUT_DIR / "guardian_bertopic_v2_document_topics.csv", index=False)


# =========================
# 6. Print summary
# =========================

print("\nDone.")
print("Topic info:")
print(topic_info)

print("\nTop words by topic:")
print(topic_words_df.groupby("topic").head(10))
