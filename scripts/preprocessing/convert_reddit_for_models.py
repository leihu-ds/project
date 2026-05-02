import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "datasets" / "reddit" / "data_reddit_public.jsonl"
OUTPUT_PATH = ROOT / "datasets" / "processed" / "reddit" / "reddit_model_ready.jsonl"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

model_ready = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)

        title = item.get("title") or ""
        selftext = item.get("selftext") or ""

        text = f"{title}\n\n{selftext}".strip()

        if len(text) < 30:
            continue

        model_ready.append({
            "source": "reddit",
            "post_id": item.get("post_id"),
            "title": title,
            "selftext": selftext,
            "text": text,
            "subreddit": item.get("subreddit"),
            "keyword": item.get("keyword"),
            "type": item.get("type"),
            "score": item.get("score"),
            "num_comments": item.get("num_comments"),
            "created_utc": item.get("created_utc"),
            "url": item.get("url"),
            "permalink": item.get("permalink"),
        })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for item in model_ready:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Input file: {INPUT_PATH}")
print(f"Model-ready records: {len(model_ready)}")
print(f"Saved to: {OUTPUT_PATH}")
