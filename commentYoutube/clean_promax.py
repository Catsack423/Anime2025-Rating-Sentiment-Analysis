import json
import re
import os

spam_phrases = [
    "nice video",
    "great video",
    "good video",
    "check my channel",
    "subscribe to my channel",
    "who is watching",
    "anyone here",
    "like if you",
]

seen_comments = set()

def clean_comment(text):

    original_text = text

    # 1 lowercase
    text = text.lower()

    # 2 remove url
    text = re.sub(r'http\S+|www\S+', '', text)

    # 3 remove emoji / symbols
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # 4 normalize repeated letters
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # 5 remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # 6 remove short comments
    if len(text.split()) < 3:
        return None

    # 7 spam phrase filtering
    for phrase in spam_phrases:
        if phrase in text:
            return None

    # 8 repeated word spam
    if re.search(r'\b(\w+)( \1){2,}', text):
        return None

    # 9 numeric spam
    if sum(c.isdigit() for c in text) > len(text) * 0.5:
        return None

    # 10 abnormal word length
    if any(len(word) > 20 for word in text.split()):
        return None

    # 11 duplicate comment
    if text in seen_comments:
        return None

    seen_comments.add(text)

    return text


BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "anime_comments_all.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_data = []

for item in data:

    cleaned = clean_comment(item["comment_text"])

    if cleaned:
        item["comment_text"] = cleaned
        cleaned_data.append(item)

output_file = os.path.join(BASE_DIR, "anime_comments_cleaned_promax.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

print("original comments:", len(data))
print("cleaned comments:", len(cleaned_data))