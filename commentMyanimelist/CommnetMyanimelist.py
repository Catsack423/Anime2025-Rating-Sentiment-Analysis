import requests
import json
import time
import os

def fetch_anime_basic(anime_id):
    try:
        api = f"https://api.jikan.moe/v4/anime/{anime_id}"
        r = requests.get(api).json()
        return {"title": r["data"].get("title")}
    except:
        return {"title": "Unknown"}

def fetch_anime_reviews_json(anime_id, target_n=10):
    results = []
    basic = fetch_anime_basic(anime_id)
    page = 1
    while len(results) < target_n:
        api = f"https://api.jikan.moe/v4/anime/{anime_id}/reviews"
        res = requests.get(api, params={"page": page})
        if res.status_code != 200: 
            print(res.status_code+": "+res.text)
            break
        data = res.json().get("data", [])
        if not data: break

        for rev in data:
            user = rev.get("user", {}) or {}
            results.append({
                "ID": rev.get("mal_id"),
                "uidpost": anime_id,
                "user_c": user.get("username"),
                "title": basic["title"],
                "text_c": rev.get("review")
            })
            if len(results) >= target_n: break
        page += 1
        time.sleep(1)
    return results

def save_to_json_list(new_data, filename="data.json"):
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
    
    if not file_exists:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
    else:
        with open(filename, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            while f.read(1) != b']':
                f.seek(-2, os.SEEK_CUR)
            f.seek(-1, os.SEEK_CUR)
            f.truncate()
            
            f.write(b",\n") 
            content = json.dumps(new_data, ensure_ascii=False, indent=2)[1:-1]
            f.write(content.encode('utf-8'))
            f.write(b"]") 

def main():
    response = requests.get("http://110.164.203.137:9919/anime")
    anime_list = response.json()

    if os.path.exists("rqs.txt"):
        with open("rqs.txt", "r") as f:
            completed_ids = set(f.read().splitlines())
    else:
        completed_ids = set()

    for item in anime_list:
        mal_id = str(item.get("mal_id"))
        if mal_id in completed_ids:
            continue

        print(f"Working on ID: {mal_id}...")
        reviews = fetch_anime_reviews_json(mal_id, 10)

        if reviews:
            save_to_json_list(reviews)
            
            with open("rqs.txt", "a") as f:
                f.write(f"{mal_id}\n")
            
            print(f"Saved {len(reviews)} reviews.")

if __name__ == "__main__":
    main()