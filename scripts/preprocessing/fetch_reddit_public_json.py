import json
import time
import requests
from pathlib import Path
from urllib.parse import quote

OUT = Path("datasets/reddit/data_reddit_public.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

KEYWORDS = [
    "circular economy",
    "recycling",
    "reuse",
    "zero waste",
    "waste reduction",
    "plastic waste",
    "sustainability",
]

SUBREDDITS = [
    "sustainability",
    "ZeroWaste",
    "environment",
    "recycling",
]

TARGET_N = 1400

HEADERS = {
    "User-Agent": "dcee-reddit-research/1.0 academic data collection"
}

records = []
seen = set()


def clean(x):
    return str(x).replace("\n", " ").replace("\r", " ").strip() if x else ""


for subreddit in SUBREDDITS:
    for keyword in KEYWORDS:
        after = None

        while len(records) < TARGET_N:
            q = quote(keyword)
            url = (
                f"https://www.reddit.com/r/{subreddit}/search.json"
                f"?q={q}&restrict_sr=1&sort=relevance&t=all&limit=100"
            )

            if after:
                url += f"&after={after}"

            print(f"Fetching r/{subreddit}: {keyword}")

            r = requests.get(url, headers=HEADERS, timeout=20)

            if r.status_code != 200:
                print("Stopped:", r.status_code, r.text[:200])
                break

            data = r.json()
            children = data.get("data", {}).get("children", [])

            if not children:
                break

            for item in children:
                post = item.get("data", {})
                post_id = post.get("id")

                if not post_id or post_id in seen:
                    continue

                seen.add(post_id)

                records.append({
                    "source": "reddit",
                    "type": "post",
                    "subreddit": subreddit,
                    "keyword": keyword,
                    "post_id": post_id,
                    "title": clean(post.get("title")),
                    "selftext": clean(post.get("selftext")),
                    "score": post.get("score"),
                    "num_comments": post.get("num_comments"),
                    "created_utc": post.get("created_utc"),
                    "url": post.get("url"),
                    "permalink": "https://www.reddit.com" + post.get("permalink", ""),
                })

                if len(records) >= TARGET_N:
                    break

            after = data.get("data", {}).get("after")

            if not after:
                break

            time.sleep(2)

        if len(records) >= TARGET_N:
            break

    if len(records) >= TARGET_N:
        break


with OUT.open("w", encoding="utf-8") as f:
    for row in records:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"Saved {len(records)} records to {OUT}")

