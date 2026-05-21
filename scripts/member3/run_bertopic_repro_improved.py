from __future__ import annotations

import argparse
import itertools
import math
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from bertopic import BERTopic
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from umap import UMAP


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "member3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TOP_N_WORDS = 10

CE_RELEVANCE_TERMS = {
    "biodiversity",
    "carbon",
    "carbonneutral",
    "circular",
    "circulareconomy",
    "clean energy",
    "climate",
    "climatechange",
    "climatecrisis",
    "compost",
    "eco",
    "emission",
    "emissions",
    "energy",
    "energytransition",
    "environment",
    "environmental",
    "fossil",
    "green",
    "hydrogen",
    "landfill",
    "net zero",
    "netzero",
    "nuclear",
    "packaging",
    "plastic",
    "pollution",
    "recyclable",
    "recycle",
    "recycled",
    "recycling",
    "renewable",
    "renewables",
    "reuse",
    "solar",
    "sustainability",
    "sustainable",
    "waste",
    "wastemanagement",
    "wind",
    "zero waste",
}

GUARDIAN_STRONG_CE_TERMS = {
    "air pollution",
    "biodiversity",
    "carbon",
    "chemical",
    "chemicals",
    "circular",
    "circulareconomy",
    "clean air",
    "clean energy",
    "climate",
    "coal",
    "emission",
    "emissions",
    "energy",
    "fossil",
    "hydrogen",
    "landfill",
    "net zero",
    "nuclear",
    "oil gas",
    "plastic",
    "pollution",
    "recyclable",
    "recycle",
    "recycled",
    "recycling",
    "renewable",
    "renewables",
    "reuse",
    "sewage",
    "solar",
    "sustainability",
    "sustainable",
    "ulez",
    "waste",
    "wildfire",
    "wildfires",
    "wind",
    "windfarm",
    "windfarms",
}

GUARDIAN_ALLOWED_SECTIONS = {
    "Australia news",
    "Business",
    "Cities",
    "Environment",
    "Global",
    "Global development",
    "Inequality",
    "Money",
    "News",
    "Opinion",
    "Politics",
    "Science",
    "Society",
    "Technology",
    "The Guardian clearing hub",
    "UK news",
    "US news",
    "World news",
}

TWITTER_SPAM_TOKENS = {
    "egcunningham",
    "gradedspa",
    "solarfred",
    "svenvanzanten",
    "svenvanzanten01",
}

TWITTER_PROMO_TOKENS = {
    "conference",
    "event",
    "join",
    "looking",
    "open",
    "register",
    "registration",
    "team",
    "thank",
    "tickets",
    "webinar",
    "workshop",
}

LANGUAGE_NOISE_TOKENS = {
    "al",
    "con",
    "de",
    "del",
    "der",
    "des",
    "di",
    "el",
    "en",
    "et",
    "il",
    "la",
    "le",
    "los",
    "per",
    "pour",
    "und",
    "une",
    "zu",
}


COMMON_STOPWORDS = {
    "said",
    "say",
    "says",
    "new",
    "year",
    "years",
    "time",
    "people",
    "like",
    "just",
    "make",
    "want",
    "need",
    "going",
    "think",
    "know",
    "told",
    "according",
    "reported",
    "today",
    "join",
    "check",
    "read",
    "watch",
    "video",
    "th",
    "amp",
    "rt",
    "http",
    "https",
    "www",
    "com",
    "2020",
    "2021",
    "2022",
    "2023",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "jan",
    "feb",
    "mar",
    "apr",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
}

PLATFORM_STOPWORDS = {
    "guardian": {
        "guardian",
        "gmt",
        "bst",
        "newsletter",
        "newsletters",
        "photograph",
        "afternoon email",
        "daily email",
        "australia",
        "australian",
    },
    "twitter": {
        "tweet",
        "twitter",
        "magazine",
        "pic",
        "thread",
        "dr",
        "mbe",
        "sven",
        "zanten",
        "svenvanzanten",
        "svenvanzanten01",
        "egcunningham",
        "graded",
        "gradedspa",
        "solarfred",
        "la",
        "di",
        "el",
        "en",
        "de",
        "le",
        "est",
        "die",
        "il",
        "des",
        "zu",
        "der",
        "une",
        "und",
        "pour",
        "con",
        "per",
        "del",
        "al",
        "im",
        "los",
    },
    "reddit": {
        "im",
        "ive",
        "dont",
        "doesnt",
        "didnt",
        "isnt",
        "cant",
        "really",
        "im",
        "thing",
        "things",
        "good",
        "use",
        "using",
    },
}


@dataclass(frozen=True)
class DatasetConfig:
    name: str
    data_path: Path
    metadata_columns: tuple[str, ...]
    min_chars: int
    paper_soo: dict[str, int]
    paper_moo: dict[str, int]
    improved: dict[str, int]


DATASETS = {
    "guardian": DatasetConfig(
        name="guardian",
        data_path=PROJECT_ROOT / "datasets" / "theguardian" / "guardian_cleaned.jsonl",
        metadata_columns=("title", "section", "date", "url"),
        min_chars=80,
        paper_soo={"n_gram": 2, "n_clusters": 2, "n_components": 5, "n_neighbors": 20},
        paper_moo={"n_gram": 1, "n_clusters": 20, "n_components": 11, "n_neighbors": 19},
        improved={"n_gram": 2, "n_clusters": 20, "n_components": 10, "n_neighbors": 20},
    ),
    "reddit": DatasetConfig(
        name="reddit",
        data_path=PROJECT_ROOT / "datasets" / "reddit" / "reddit_cleaned.jsonl",
        metadata_columns=("post_id", "title", "subreddit", "created_utc", "url"),
        min_chars=40,
        paper_soo={"n_gram": 2, "n_clusters": 2, "n_components": 15, "n_neighbors": 20},
        paper_moo={"n_gram": 1, "n_clusters": 14, "n_components": 13, "n_neighbors": 15},
        improved={"n_gram": 2, "n_clusters": 14, "n_components": 13, "n_neighbors": 15},
    ),
    "twitter": DatasetConfig(
        name="twitter",
        data_path=PROJECT_ROOT / "datasets" / "twitter" / "twitter_cleaned.jsonl",
        metadata_columns=("tweet_id", "url", "recovery_method"),
        min_chars=30,
        paper_soo={"n_gram": 2, "n_clusters": 10, "n_components": 10, "n_neighbors": 10},
        paper_moo={"n_gram": 1, "n_clusters": 8, "n_components": 7, "n_neighbors": 15},
        improved={"n_gram": 2, "n_clusters": 8, "n_components": 7, "n_neighbors": 15},
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run reproducible BERTopic experiments for Member 3."
    )
    parser.add_argument(
        "--dataset",
        choices=["guardian", "reddit", "twitter", "all"],
        default="all",
        help="Dataset to model.",
    )
    parser.add_argument(
        "--mode",
        choices=["paper-soo", "paper-moo", "improved", "grid-search"],
        default="improved",
        help=(
            "paper-soo reproduces paper Table 2, paper-moo reproduces paper Table 3, "
            "improved uses stronger cleaning/deduplication, grid-search evaluates "
            "the paper SOO grid with the local C_NPMI implementation."
        ),
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Optional sample size for quick tests.",
    )
    return parser.parse_args()


def normalise_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def has_ce_signal(text: str) -> bool:
    return any(contains_term(text, term) for term in CE_RELEVANCE_TERMS)


def token_set(text: str) -> set[str]:
    return set(text.split())


def is_twitter_quality_doc(text: str) -> bool:
    tokens = token_set(text)
    if tokens & TWITTER_SPAM_TOKENS:
        return False

    if len(tokens & LANGUAGE_NOISE_TOKENS) >= 2:
        return False

    # Keep event-related tweets only when they still carry a strong CE signal.
    promo_hits = len(tokens & TWITTER_PROMO_TOKENS)
    if promo_hits >= 2 and not has_ce_signal(text):
        return False

    # Very short tweets dominated by announcements tend to form generic
    # register/team/thank topics instead of substantive CE themes.
    if promo_hits >= 3 and len(tokens) < 22:
        return False

    return has_ce_signal(text)


def is_guardian_quality_doc(text: str) -> bool:
    return any(contains_term(text, term) for term in GUARDIAN_STRONG_CE_TERMS)


def apply_quality_filters(
    df: pd.DataFrame, dataset_name: str, mode: str
) -> pd.DataFrame:
    if mode not in {"improved", "grid-search"}:
        return df

    if dataset_name == "twitter":
        mask = df["model_text"].map(is_twitter_quality_doc)
    elif dataset_name == "guardian":
        mask = df["model_text"].map(is_guardian_quality_doc)
        if "section" in df.columns:
            mask = mask & df["section"].isin(GUARDIAN_ALLOWED_SECTIONS)
    else:
        return df

    removed = int((~mask).sum())
    print(f"Removed {dataset_name} quality-filtered rows: {removed}")
    return df[mask].copy()


def load_documents(config: DatasetConfig, mode: str, sample: int | None) -> pd.DataFrame:
    print(f"Loading {config.name}: {config.data_path}")
    df = pd.read_json(config.data_path, lines=True)
    print(f"Rows before filtering: {len(df)}")

    if "clean_text" not in df.columns:
        raise ValueError(f"{config.data_path} does not contain a clean_text column.")

    df = df.dropna(subset=["clean_text"]).copy()
    df["clean_text"] = df["clean_text"].astype(str)

    if "clean_text_length" in df.columns:
        df = df[df["clean_text_length"] > 20].copy()

    df["model_text"] = df["clean_text"].map(normalise_text)
    df = df[df["model_text"].str.len() >= config.min_chars].copy()

    if mode in {"improved", "grid-search"}:
        before = len(df)
        df = df.drop_duplicates(subset=["model_text"]).copy()
        print(f"Removed exact duplicate model texts: {before - len(df)}")
        df = apply_quality_filters(df, config.name, mode)

    if sample is not None and len(df) > sample:
        df = df.sample(sample, random_state=RANDOM_STATE).copy()
        print(f"Sampled rows: {len(df)}")

    print(f"Rows used: {len(df)}")
    return df.reset_index(drop=True)


def stop_words_for(dataset: str, mode: str) -> list[str] | str:
    if mode in {"paper-soo", "paper-moo"}:
        return "english"

    stop_words = set(ENGLISH_STOP_WORDS)
    stop_words.update(COMMON_STOPWORDS)
    stop_words.update(PLATFORM_STOPWORDS[dataset])
    return sorted(stop_words)


def build_topic_model(dataset: str, params: dict[str, int], mode: str) -> BERTopic:
    max_ngram = params["n_gram"]
    vectorizer_model = CountVectorizer(
        ngram_range=(1, max_ngram),
        stop_words=stop_words_for(dataset, mode),
        min_df=2 if mode == "improved" else 1,
        max_df=0.85 if mode == "improved" else 1.0,
    )
    umap_model = UMAP(
        n_neighbors=params["n_neighbors"],
        n_components=params["n_components"],
        random_state=RANDOM_STATE,
    )
    cluster_model = KMeans(
        n_clusters=params["n_clusters"],
        random_state=RANDOM_STATE,
        n_init=10,
    )
    return BERTopic(
        vectorizer_model=vectorizer_model,
        umap_model=umap_model,
        hdbscan_model=cluster_model,
        calculate_probabilities=False,
        top_n_words=TOP_N_WORDS,
        verbose=True,
    )


def extract_topic_words(topic_model: BERTopic, topic_info: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for topic_id in topic_info["Topic"]:
        if topic_id == -1:
            continue
        words = topic_model.get_topic(topic_id) or []
        for word, score in words:
            rows.append({"topic": int(topic_id), "word": word, "score": score})
    return pd.DataFrame(rows)


def contains_term(doc: str, term: str) -> bool:
    # Terms can be unigrams or n-grams. Word-boundary regex keeps phrase matching
    # robust without requiring a second vectorizer pass for every candidate topic.
    return re.search(rf"(?<![a-z]){re.escape(term)}(?![a-z])", doc) is not None


def c_npmi(documents: list[str], topic_words_df: pd.DataFrame, top_n: int = TOP_N_WORDS) -> float:
    if topic_words_df.empty:
        return float("nan")

    n_docs = len(documents)
    if n_docs == 0:
        return float("nan")

    scores = []
    for _, group in topic_words_df.groupby("topic"):
        words = group.sort_values("score", ascending=False)["word"].head(top_n).tolist()
        if len(words) < 2:
            continue

        presence = {
            word: [contains_term(doc, word) for doc in documents]
            for word in words
        }

        pair_scores = []
        for w1, w2 in itertools.combinations(words, 2):
            df1 = sum(presence[w1])
            df2 = sum(presence[w2])
            df12 = sum(a and b for a, b in zip(presence[w1], presence[w2]))
            if df1 == 0 or df2 == 0 or df12 == 0:
                pair_scores.append(-1.0)
                continue
            p1 = df1 / n_docs
            p2 = df2 / n_docs
            p12 = df12 / n_docs
            pmi = math.log(p12 / (p1 * p2))
            pair_scores.append(pmi / -math.log(p12))

        if pair_scores:
            scores.append(sum(pair_scores) / len(pair_scores))

    return sum(scores) / len(scores) if scores else float("nan")


def topic_diversity(topic_words_df: pd.DataFrame, top_n: int = TOP_N_WORDS) -> float:
    selected = []
    for _, group in topic_words_df.groupby("topic"):
        selected.extend(group.sort_values("score", ascending=False)["word"].head(top_n).tolist())
    if not selected:
        return float("nan")
    return len(set(selected)) / len(selected)


def save_outputs(
    config: DatasetConfig,
    mode: str,
    params: dict[str, int],
    df: pd.DataFrame,
    topics: list[int],
    topic_info: pd.DataFrame,
    topic_words_df: pd.DataFrame,
) -> None:
    prefix = f"{config.name}_bertopic_{mode.replace('-', '_')}"

    topic_info_to_save = topic_info.copy()
    if "Representative_Docs" in topic_info_to_save.columns:
        def compact_docs(docs: object) -> object:
            if not isinstance(docs, list):
                return docs
            compacted = []
            for doc in docs[:3]:
                doc = re.sub(r"\s+", " ", str(doc)).strip()
                compacted.append(doc[:240])
            return " | ".join(compacted)

        topic_info_to_save["Representative_Docs"] = topic_info_to_save[
            "Representative_Docs"
        ].map(compact_docs)

    topic_info_to_save.to_csv(OUTPUT_DIR / f"{prefix}_topic_info.csv", index=False)
    topic_words_df.to_csv(OUTPUT_DIR / f"{prefix}_topic_words.csv", index=False)

    metadata_columns = [col for col in config.metadata_columns if col in df.columns]
    doc_topics = df[metadata_columns].copy()
    doc_topics["model_text"] = df["model_text"]
    doc_topics["topic"] = topics
    doc_topics.to_csv(OUTPUT_DIR / f"{prefix}_document_topics.csv", index=False)

    metrics = {
        "dataset": config.name,
        "mode": mode,
        **params,
        "documents": len(df),
        "topics": int(topic_info[topic_info["Topic"] != -1]["Topic"].nunique()),
        "c_npmi": c_npmi(df["model_text"].tolist(), topic_words_df),
        "topic_diversity": topic_diversity(topic_words_df),
    }
    pd.DataFrame([metrics]).to_csv(OUTPUT_DIR / f"{prefix}_metrics.csv", index=False)
    print("Metrics:")
    print(pd.Series(metrics).to_string())


def params_for(config: DatasetConfig, mode: str) -> dict[str, int]:
    if mode == "paper-soo":
        return dict(config.paper_soo)
    if mode == "paper-moo":
        return dict(config.paper_moo)
    if mode == "improved":
        return dict(config.improved)
    raise ValueError(f"Mode {mode} does not have a single parameter set.")


def run_single(config: DatasetConfig, mode: str, sample: int | None) -> None:
    df = load_documents(config, mode, sample)
    documents = df["model_text"].tolist()
    params = params_for(config, mode)
    print(f"Training {config.name} / {mode} with params: {params}")
    topic_model = build_topic_model(config.name, params, mode)
    topics, _ = topic_model.fit_transform(documents)
    topic_info = topic_model.get_topic_info()
    topic_words_df = extract_topic_words(topic_model, topic_info)
    save_outputs(config, mode, params, df, topics, topic_info, topic_words_df)


def grid_search(config: DatasetConfig, sample: int | None) -> None:
    df = load_documents(config, "grid-search", sample)
    documents = df["model_text"].tolist()
    search_space = {
        "n_gram": [1, 2, 3],
        "n_clusters": [2, 5, 10, 15, 20, 25],
        "n_components": [5, 10, 15],
        "n_neighbors": [10, 15, 20],
    }

    rows = []
    keys = list(search_space)
    for values in itertools.product(*(search_space[key] for key in keys)):
        params = dict(zip(keys, values))
        print(f"Grid candidate {config.name}: {params}")
        topic_model = build_topic_model(config.name, params, "improved")
        topics, _ = topic_model.fit_transform(documents)
        topic_info = topic_model.get_topic_info()
        topic_words_df = extract_topic_words(topic_model, topic_info)
        rows.append(
            {
                **params,
                "documents": len(df),
                "topics": int(topic_info[topic_info["Topic"] != -1]["Topic"].nunique()),
                "c_npmi": c_npmi(documents, topic_words_df),
                "topic_diversity": topic_diversity(topic_words_df),
            }
        )

    result = pd.DataFrame(rows).sort_values(
        ["c_npmi", "topic_diversity"], ascending=[False, False]
    )
    out_path = OUTPUT_DIR / f"{config.name}_bertopic_grid_search_metrics.csv"
    result.to_csv(out_path, index=False)
    print(f"Saved grid search metrics: {out_path}")
    print(result.head(10).to_string(index=False))


def main() -> None:
    args = parse_args()
    selected = DATASETS.keys() if args.dataset == "all" else [args.dataset]
    for dataset_name in selected:
        config = DATASETS[dataset_name]
        if args.mode == "grid-search":
            grid_search(config, args.sample)
        else:
            run_single(config, args.mode, args.sample)


if __name__ == "__main__":
    main()
