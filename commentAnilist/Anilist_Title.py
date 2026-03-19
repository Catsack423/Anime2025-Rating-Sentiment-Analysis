import requests
import time
import json
import os

URL = "https://graphql.anilist.co"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (AniListSafeCrawler/1.0)"
}

OUT_FILE = "anime_2025_all_new.json"
CHECKPOINT_FILE = "checkpoint.json"

DELAY = 1.5
MAX_RETRY = 3

YEARS = [2025]

QUERY = """
query ($page: Int, $year: Int) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      hasNextPage
    }
    media(type: ANIME, seasonYear: $year) {
      id
      title { romaji }
      seasonYear
      format
    }
  }
}
"""

if os.path.exists(OUT_FILE):
    with open(OUT_FILE, "r", encoding="utf-8") as f:
        all_anime = json.load(f)
else:
    all_anime = []

if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
        checkpoint = json.load(f)
else:
    checkpoint = {
        "year_index": 0,
        "page": 1
    }

year_index = checkpoint["year_index"]
page = checkpoint["page"]

while year_index < len(YEARS):
    year = YEARS[year_index]
    retry = 0

    print(f"\nYear {year} | page {page}")

    res = requests.post(
        URL,
        json={"query": QUERY, "variables": {"page": page, "year": year}},
        headers=HEADERS
    )

    data = res.json()

    if data.get("data") is None:
        retry += 1
        print("block / rate limit")

        if retry >= MAX_RETRY:
            print("หยุดเพื่อความปลอดภัย (รันใหม่ภายหลัง)")
            break

        time.sleep(5)
        continue

    retry = 0

    media = data["data"]["Page"]["media"]
    has_next = data["data"]["Page"]["pageInfo"]["hasNextPage"]

    all_anime.extend(media)
    print(f"+{len(media)} | รวม {len(all_anime)}")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_anime, f, ensure_ascii=False, indent=2)

    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "year_index": year_index,
            "page": page
        }, f)

    if not has_next:
        print(f"ปี {year} ครบแล้ว")
        year_index += 1
        page = 1
    else:
        page += 1

    time.sleep(DELAY)

print("\n FINISHED")
print("Total anime:", len(all_anime))
print("Saved to:", OUT_FILE)
