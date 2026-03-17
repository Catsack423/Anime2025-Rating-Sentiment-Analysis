import json
import re
import os

spam_words = [
    "nice video",
    "great video",
    "good video",
    "check my channel",
    "subscribe to my channel"
]

seen_comments = set()

def clean_comment(text):

    text = text.lower()

    text = re.sub(r'http\S+|www\S+', '', text)

    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    text = re.sub(r'\s+', ' ', text).strip()

    if len(text.split()) < 3:
        return None

    for word in spam_words:
        if word in text:
            return None

    if re.search(r'\b(\w+)( \1){2,}', text):
        return None

    if text in seen_comments:
        return None

    seen_comments.add(text)

    return text


BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "anime_comments_all.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

filtered_data = []

for item in data:

    cleaned = clean_comment(item["comment_text"])

    if cleaned:
        item["comment_text"] = cleaned
        filtered_data.append(item)

output_path = os.path.join(BASE_DIR, "comments_yt_cleaned.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print("cleaned comments:", len(filtered_data))