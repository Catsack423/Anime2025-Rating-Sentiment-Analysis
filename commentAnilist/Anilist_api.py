import requests
import time
import json
import os

URL = "https://graphql.anilist.co"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (AnimeThreadResearchBot/1.0)"
}

START_INDEX = 0
LIMIT = 1000
DELAY = 6
SMALL_DELAY = 2 

INPUT_FILE = "anime_2025_all_new.json"
OUTPUT_FILE = "anime_2025_thread_comments_new.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    anime_all = json.load(f)

anime_batch = anime_all[START_INDEX:START_INDEX + LIMIT]

print(f"Processing {len(anime_batch)} anime ({START_INDEX} → {START_INDEX + len(anime_batch) - 1})")

if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        rows = json.load(f)
else:
    rows = []

existing_keys = set(
    (r.get("anime_id"), r.get("thread_id"), r.get("user"), r.get("text"))
    for r in rows
)

thread_query = """
query ($mediaId: Int) {
  Page(page: 1, perPage: 5) {
    threads(mediaCategoryId: $mediaId) {
      id
      title
    }
  }
}
"""

comment_query = """
query ($threadId: Int) {
  Page(page: 1, perPage: 20) {
    threadComments(threadId: $threadId) {
      id
      comment
      user { name }
    }
  }
}
"""

for i, anime in enumerate(anime_batch, start=START_INDEX + 1):
    anime_id = anime["id"]
    title = anime["title"]["romaji"]

    print(f"\n[{i}] {title}")

    try:
        res_thread = requests.post(
            URL,
            json={"query": thread_query, "variables": {"mediaId": anime_id}},
            headers=HEADERS,
            timeout=20
        )

        thread_data = res_thread.json()

        if not thread_data.get("data"):
            print("No thread data")
            time.sleep(DELAY)
            continue

        threads = thread_data["data"]["Page"]["threads"]

        print(f"Threads found: {len(threads)}")

        for thread in threads:
            thread_id = thread["id"]
            thread_title = thread["title"]

            res_comment = requests.post(
                URL,
                json={"query": comment_query, "variables": {"threadId": thread_id}},
                headers=HEADERS,
                timeout=20
            )

            comment_data = res_comment.json()

            if not comment_data.get("data"):
                continue

            comments = comment_data["data"]["Page"]["threadComments"]

            print(f"{len(comments)} comments")

            for c in comments:
                key = (anime_id, thread_id, c["user"]["name"], c["comment"])

                if key not in existing_keys:
                    rows.append({
                        "anime": title,
                        "anime_id": anime_id,
                        "thread_id": thread_id,
                        "thread_title": thread_title,
                        "user": c["user"]["name"],
                        "text": c["comment"]
                    })
                    existing_keys.add(key)

            time.sleep(SMALL_DELAY)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

        print(f"Saved ({len(rows)} total comments)")

        time.sleep(DELAY)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(DELAY * 2)

print("\nDONE")
print("Total comments saved:", len(rows))
print("Output file:", OUTPUT_FILE)
