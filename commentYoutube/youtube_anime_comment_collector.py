import os
import csv
import time
import requests
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


YOUTUBE_API_KEYS = [
    "AIzaSyBF7TKejJDBmH9_WE5ZARqmBon7x7kx9HM",
    "AIzaSyALpSJGnQLCRreo2PpBIZVFoSkViUg93xA",
    "AIzaSyAgFM09BYl6mmuX0yAg5tNICcsHkL7JxFg"
]

ANIME_API_URL = "http://110.164.203.137:9919/anime"
JSON_PATH = os.path.join(os.getcwd(), "anime_comments_all.jsonl")

MAX_VIDEOS_PER_ANIME = 3
MAX_COMMENTS_PER_VIDEO = 50
SLEEP_BETWEEN_CALLS = 1

class YouTubeKeyManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.index = 0
        self.youtube = self._build()

    def _build(self):
        print(f"Using API KEY #{self.index + 1}")
        return build("youtube", "v3", developerKey=self.api_keys[self.index])

    def switch_key(self):
        self.index += 1
        if self.index >= len(self.api_keys):
            raise RuntimeError("All YouTube API keys exhausted")
        self.youtube = self._build()

    def get(self):
        return self.youtube

def safe_execute(key_mgr, func):
    while True:
        try:
            return func(key_mgr.get())

        except HttpError as e:
            if "quotaExceeded" in str(e):
                print("quotaExceeded → switch API key")
                key_mgr.switch_key()
            elif "commentsDisabled" in str(e):
                return None
            else:
                print("HttpError:", e)
                time.sleep(3)

        except (requests.exceptions.RequestException,
                TimeoutError,
                ConnectionError) as e:

            print("Network error → retrying in 5s")
            print(e)
            time.sleep(5)

        except Exception as e:
            print("Unexpected error:", e)
            time.sleep(5)

def load_checkpoint():
    done_anime, done_video, done_comment = set(), set(), set()

    if not os.path.exists(JSON_PATH):
        return done_anime, done_video, done_comment

    with open(JSON_PATH, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            done_anime.add(row["anime_name"])
            done_video.add(row["video_id"])
            done_comment.add(row["comment_id"])

    print(f"♻ Resume | Anime:{len(done_anime)} Video:{len(done_video)} Comment:{len(done_comment)}")
    return done_anime, done_video, done_comment
 
def save_row(row):
    with open(JSON_PATH, "a", encoding="utf-8") as f:
        json.dump(row, f, ensure_ascii=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())

def fetch_anime_list():
    res = requests.get(ANIME_API_URL, timeout=10)
    res.raise_for_status()
    return [a.get("anime_name") or a.get("title") for a in res.json() if a]

def fetch_comments(key_mgr, anime, video_id, done_comment):
    count = 0
    next_page = None

    while True:
        res = safe_execute(
            key_mgr,
            lambda yt: yt.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page,
                textFormat="plainText"
            ).execute()
        )

        if not res:
            return

        for item in res.get("items", []):
            c = item["snippet"]["topLevelComment"]
            cid = c["id"]
            if cid in done_comment:
                continue

            s = c["snippet"]
            save_row({
                "anime_name": anime,
                "video_id": video_id,
                "comment_id": cid,
                "author": s["authorDisplayName"],
                "comment_text": s["textDisplay"],
                "like_count": s["likeCount"],
                "published_at": s["publishedAt"]
            })

            done_comment.add(cid)
            count += 1
            if count >= MAX_COMMENTS_PER_VIDEO:
                return

        next_page = res.get("nextPageToken")
        if not next_page:
            return

def main():
    key_mgr = YouTubeKeyManager(YOUTUBE_API_KEYS)
    done_anime, done_video, done_comment = load_checkpoint()

    anime_list = fetch_anime_list()
    print(f"Total anime: {len(anime_list)}")

    for anime in anime_list:
        if anime in done_anime:
            continue

        print(f"\nAnime: {anime}")

        res = safe_execute(
            key_mgr,
            lambda yt: yt.search().list(
                q=f"#{anime}",
                part="id",
                type="video",
                maxResults=MAX_VIDEOS_PER_ANIME
            ).execute()
        )

        if not res:
            continue

        for v in res.get("items", []):
            vid = v.get("id", {}).get("videoId")
            if not vid:
                continue

            if vid in done_video:
                continue

            print(f"▶ Video: {vid}")
            fetch_comments(key_mgr, anime, vid, done_comment)
            done_video.add(vid)
            time.sleep(SLEEP_BETWEEN_CALLS)

        done_anime.add(anime)

    print("\n DONE")
if __name__ == "__main__":
    main()
