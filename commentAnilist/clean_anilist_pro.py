import json
import re
import os

spam_phrases = [
    "nice video", "great video", "check my channel", 
    "subscribe to", "who is watching", "anyone here",
    "like if you", "best girl", "peak fiction",
]

seen_comments = set()

def clean_comment(text):
    if not text:
        return None

    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9ก-๙\s]', ' ', text)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    lower_text = text.lower()
    
    if len(text.split()) < 3:
        return None
    
    for phrase in spam_phrases:
        if phrase in lower_text:
            return None
            
    if sum(c.isdigit() for c in text) > len(text) * 0.5:
        return None
    
    if lower_text in seen_comments:
        return None
    seen_comments.add(lower_text)

    return text

INPUT_FILE = "commentAnilist/clean_comment_anilst.json"
OUTPUT_FILE = "commentAnilist/cleaned_anime_comments_pro.json"

if os.path.exists(INPUT_FILE):
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = []
    for item in data:
        cleaned_text = clean_comment(item.get("text", ""))
        
        if cleaned_text:
            new_item = item.copy()
            new_item["text"] = cleaned_text
            cleaned_data.append(new_item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
    print(f"เสร็จสิ้น! กรองข้อมูลเหลือ {len(cleaned_data)} จาก {len(data)} รายการ")
else:
    print(f"ไม่พบไฟล์: {INPUT_FILE}")