import json
import re
import time
import html
from pathlib import Path

import requests
from bs4 import BeautifulSoup

INPUT = Path("datasets/twitter/data_twitter.json")
OUTPUT = Path("datasets/twitter/twitter_recovered_text.jsonl")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; academic-data-recovery/1.0)"
}

def load_items(path):
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("["):
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]

def normalize_url(url):
    if not url:
        return None
    url = url.replace("x.com/", "twitter.com/")
    return url.split("?")[0]

def extract_tweet_id(url):
    m = re.search(r"/status/(\d+)", url or "")
    return m.group(1) if m else None

def clean_text(s):
    if not s:
        return None
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or None

def recover_from_oembed(url):
    endpoint = "https://publish.twitter.com/oembed"
    r = requests.get(endpoint, params={"url": url, "omit_script": "true"}, headers=HEADERS, timeout=20)

    if r.status_code != 200:
        return None, f"oembed_status_{r.status_code}"

    data = r.json()
    embed_html = data.get("html", "")
    soup = BeautifulSoup(embed_html, "html.parser")

    blockquote = soup.find("blockquote")
    if not blockquote:
        return None, "oembed_no_blockquote"

    text = blockquote.get_text(" ", strip=True)
    text = re.sub(r"https://t\.co/\S+", "", text)
    text = clean_text(text)

    return text, None if text else "oembed_empty_text"

def get_wayback_snapshot(url):
    cdx = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": url,
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype",
        "filter": "statuscode:200",
        "collapse": "digest",
        "limit": "1",
    }

    try:
        r = requests.get(cdx, params=params, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return None

        data = r.json()
        if len(data) < 2:
            return None

        timestamp, original, statuscode, mimetype = data[1]
        return f"https://web.archive.org/web/{timestamp}/{original}"
    except Exception:
        return None

    data = r.json()
    if len(data) < 2:
        return None

    timestamp, original, statuscode, mimetype = data[1]
    return f"https://web.archive.org/web/{timestamp}/{original}"

def recover_from_wayback(url):
    snapshot = get_wayback_snapshot(url)
    if not snapshot:
        return None, "wayback_no_snapshot"

    try:
        r = requests.get(snapshot, headers=HEADERS, timeout=25)
    except Exception as e:
        return None, f"wayback_request_error_{type(e).__name__}"

    if r.status_code != 200:
        return None, f"wayback_status_{r.status_code}"

    soup = BeautifulSoup(r.text, "html.parser")

    candidates = []

    for tag in soup.find_all(["p", "div", "span"]):
        txt = clean_text(tag.get_text(" ", strip=True))
        if txt and len(txt) > 30:
            candidates.append(txt)

    candidates = [
        c for c in candidates
        if "JavaScript is not available" not in c
        and "Log in" not in c
        and "Sign up" not in c
        and "Twitter" not in c[:20]
    ]

    if not candidates:
        return None, "wayback_no_text"

    return max(candidates, key=len), None

def main():
    items = load_items(INPUT)
    print(f"Loaded {len(items)} twitter records")

    done_ids = set()
    if OUTPUT.exists():
        for line in OUTPUT.read_text(encoding="utf-8").splitlines():
            try:
                obj = json.loads(line)
                if obj.get("tweet_id"):
                    done_ids.add(obj["tweet_id"])
            except Exception:
                pass

    with OUTPUT.open("a", encoding="utf-8") as out:
        for i, item in enumerate(items, 1):
            raw_url = item.get("url") or item.get("tweet_url") or item.get("expanded_url")
            url = normalize_url(raw_url)
            tweet_id = extract_tweet_id(url)

            if not url or not tweet_id:
                continue

            if tweet_id in done_ids:
                continue

            result = {
                "tweet_id": tweet_id,
                "url": url,
                "text": None,
                "method": None,
                "error": None,
            }

            print(f"[{i}/{len(items)}] {url}")

            text, err = recover_from_oembed(url)
            if text:
                result["text"] = text
                result["method"] = "oembed"
            else:
                text, err2 = recover_from_wayback(url)
                if text:
                    result["text"] = text
                    result["method"] = "wayback"
                else:
                    result["error"] = f"{err}; {err2}"

            out.write(json.dumps(result, ensure_ascii=False) + "\n")
            out.flush()

            time.sleep(2)

if __name__ == "__main__":
    main()
