import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "datasets" / "theguardian" / "data_guardian.json"
OUTPUT_PATH = ROOT / "datasets" / "processed" / "guardian" / "guardian_3000_with_text.json"
PROGRESS_PATH = ROOT / "datasets" / "processed" / "guardian" / "guardian_3000_progress.json"

TARGET_N = 3000
SLEEP_SECONDS = 1.2

API_KEY = os.getenv("GUARDIAN_API_KEY")
if not API_KEY:
    raise RuntimeError("GUARDIAN_API_KEY is not set. Run: export GUARDIAN_API_KEY='your_key_here'")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def guardian_path_from_url(url):
    parsed = urlparse(url)
    return parsed.path.lstrip("/")


def load_json(path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


def count_ok_records(records):
    return len([x for x in records if x.get("fetch_status") == "ok" and x.get("body")])


def fetch_article(url):
    path = guardian_path_from_url(url)
    api_url = f"https://content.guardianapis.com/{path}"

    params = {
        "api-key": API_KEY,
        "show-fields": "headline,bodyText",
    }

    response = requests.get(api_url, params=params, timeout=30)

    if response.status_code == 404:
        return {
            "fetch_status": "not_found",
            "title": None,
            "body": None,
        }

    if response.status_code == 429:
        raise RuntimeError("Rate limit reached. Stop now and continue later.")

    response.raise_for_status()

    data = response.json()
    content = data.get("response", {}).get("content", {})
    fields = content.get("fields", {})

    return {
        "fetch_status": "ok",
        "title": fields.get("headline"),
        "body": fields.get("bodyText"),
    }


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        source_records = json.load(f)

    output = load_json(OUTPUT_PATH, [])
    progress = load_json(PROGRESS_PATH, {"done_urls": []})
    done_urls = set(progress.get("done_urls", []))

    print(f"Input records: {len(source_records)}")
    print(f"Already saved records: {len(output)}")
    print(f"Already tried URLs: {len(done_urls)}")
    print(f"Records with body: {count_ok_records(output)}")
    print(f"Target records with body: {TARGET_N}")

    for item in source_records:
        if count_ok_records(output) >= TARGET_N:
            break

        url = item.get("url")
        if not url or url in done_urls:
            continue

        print(f"\nFetching URL {len(done_urls) + 1}: {url}")

        new_item = dict(item)

        try:
            fetched = fetch_article(url)
            new_item.update(fetched)

            if new_item.get("body"):
                print(f"OK: {new_item.get('title')}")
                print(f"Body length: {len(new_item.get('body'))}")
            else:
                print(f"No body. Status: {new_item.get('fetch_status')}")

        except Exception as e:
            new_item["fetch_status"] = "error"
            new_item["title"] = None
            new_item["body"] = None
            new_item["error"] = str(e)
            print(f"ERROR: {e}")

            if "Rate limit" in str(e):
                save_json(OUTPUT_PATH, output)
                progress["done_urls"] = list(done_urls)
                save_json(PROGRESS_PATH, progress)
                print("Saved progress before stopping.")
                return

        output.append(new_item)
        done_urls.add(url)

        save_json(OUTPUT_PATH, output)
        progress["done_urls"] = list(done_urls)
        save_json(PROGRESS_PATH, progress)

        print(f"Current records with body: {count_ok_records(output)}")

        time.sleep(SLEEP_SECONDS)

    print("\nFinished for now.")
    print(f"Saved file: {OUTPUT_PATH}")
    print(f"Records saved: {len(output)}")
    print(f"Records with body: {count_ok_records(output)}")


if __name__ == "__main__":
    main()
