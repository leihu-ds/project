import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "datasets" / "processed" / "guardian" / "guardian_3000_with_text.json"
OUTPUT_PATH = ROOT / "datasets" / "processed" / "guardian" / "guardian_model_ready.jsonl"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

model_ready = []

for item in data:
    title = item.get("title")
    body = item.get("body")

    if not title or not body:
        continue

    model_ready.append({
        "title": title,
        "section": item.get("section"),
        "date": item.get("date"),
        "url": item.get("url"),
        "content": {
            "body": body
        }
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for item in model_ready:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Input records: {len(data)}")
print(f"Model-ready records: {len(model_ready)}")
print(f"Saved to: {OUTPUT_PATH}")
