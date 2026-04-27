from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]

DATA_FILES = [
    ROOT / "datasets" / "theguardian" / "data_guardian.json",
    ROOT / "datasets" / "reddit" / "data_reddit.json",
    ROOT / "datasets" / "twitter" / "data_twitter.json",
    ROOT / "datasets" / "twitter" / "data_twitter_external_links.json",
    ROOT / "datasets" / "twitter" / "data_twitter_related_ids.json",
]

def preview_value(value, max_len=150):
    text = str(value).replace("\n", " ")
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text

def inspect_file(path: Path):
    print(f"\n{'=' * 80}")
    print(f"FILE: {path.relative_to(ROOT)}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Top-level type: {type(data).__name__}")

    if not isinstance(data, list):
        print("This file is not a list. Skipping detailed record inspection.")
        return

    print(f"Records: {len(data)}")

    key_counter = Counter()
    for record in data:
        if isinstance(record, dict):
            key_counter.update(record.keys())

    print("\nAll keys and occurrence counts:")
    for key, count in key_counter.most_common():
        print(f"- {key}: {count}")

    print("\nFirst non-empty sample values by key:")
    shown = set()
    for record in data:
        if not isinstance(record, dict):
            continue
        for key, value in record.items():
            if key in shown:
                continue
            if value not in [None, "", [], {}]:
                print(f"- {key}: {preview_value(value)}")
                shown.add(key)
        if len(shown) == len(key_counter):
            break

def main():
    for path in DATA_FILES:
        if path.exists():
            inspect_file(path)
        else:
            print(f"\nMissing file: {path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
