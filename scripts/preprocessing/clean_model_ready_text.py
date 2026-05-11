import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INPUT_FILES = {
    "guardian": ROOT / "datasets" / "processed" / "guardian" / "guardian_model_ready.jsonl",
    "reddit": ROOT / "datasets" / "processed" / "reddit" / "reddit_model_ready.jsonl",
    "twitter": ROOT / "datasets" / "twitter" / "twitter_for_models.jsonl",
}

OUTPUT_DIR = ROOT / "datasets" / "processed" / "cleaned"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILES = {
    "guardian": OUTPUT_DIR / "guardian_cleaned.jsonl",
    "reddit": OUTPUT_DIR / "reddit_cleaned.jsonl",
    "twitter": OUTPUT_DIR / "twitter_cleaned.jsonl",
}

URL_RE = re.compile(r"https?://\S+|www\.\S+")
PIC_TWITTER_RE = re.compile(r"pic\.twitter\.com/\S+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text):
    if text is None:
        return ""

    text = str(text)
    text = html.unescape(text)
    text = HTML_TAG_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = PIC_TWITTER_RE.sub(" ", text)
    text = text.replace("\u00a0", " ")
    text = text.replace("\ufeff", " ")
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()


def get_raw_text(source, item):
    if source == "guardian":
        title = item.get("title") or ""
        body = item.get("content", {}).get("body") or ""
        return f"{title}. {body}".strip()

    if source == "reddit":
        title = item.get("title") or ""
        selftext = item.get("selftext") or ""
        return item.get("text") or f"{title}\n\n{selftext}".strip()

    if source == "twitter":
        return item.get("text") or ""

    return ""


def clean_file(source, input_path, output_path):
    if not input_path.exists():
        print(f"Missing input file for {source}: {input_path}")
        return

    input_count = 0
    output_count = 0

    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue

            input_count += 1
            item = json.loads(line)

            raw_text = get_raw_text(source, item)
            cleaned = clean_text(raw_text)

            if len(cleaned) < 30:
                continue

            item["clean_text"] = cleaned
            item["clean_text_length"] = len(cleaned)

            fout.write(json.dumps(item, ensure_ascii=False) + "\n")
            output_count += 1

    print(f"{source}:")
    print(f"  input records: {input_count}")
    print(f"  cleaned records: {output_count}")
    print(f"  output file: {output_path}")


def main():
    for source, input_path in INPUT_FILES.items():
        clean_file(source, input_path, OUTPUT_FILES[source])


if __name__ == "__main__":
    main()

