import json
import re
import os

# รายการคำหรือประโยคที่มักจะเป็นสแปม (ปรับแต่งเพิ่มได้)
spam_phrases = [
    "nice video", "great video", "check my channel", 
    "subscribe to", "who is watching", "anyone here",
    "like if you", "best girl", "peak fiction", # ตัวอย่างคำมัวๆ ในวงการอนิเมะ
]

seen_comments = set()

def clean_comment(text):
    if not text:
        return None
    
    # 1. ลบ URL / เว็บไซต์ (ทั้ง http และ www)
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # 2. ลบอิโมจิ และสัญลักษณ์พิเศษ (เก็บไว้เฉพาะตัวอักษรและตัวเลข)
    # ปรับปรุงให้รองรับภาษาไทยและภาษาอังกฤษ
    text = re.sub(r'[^a-zA-Z0-9ก-๙\s]', ' ', text)
    
    # 3. จัดการตัวอักษรซ้ำๆ มากเกินไป (เช่น "555555" -> "55")
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    
    # 4. ลบช่องว่างส่วนเกิน
    text = re.sub(r'\s+', ' ', text).strip()
    
    # แปลงเป็นตัวพิมพ์เล็กเพื่อตรวจสอบสแปมได้ง่ายขึ้น
    lower_text = text.lower()
    
    # 5. กรองคอมเมนต์สั้นเกินไป (น้อยกว่า 3 คำ)
    if len(text.split()) < 3:
        return None
    
    # 6. กรองประโยคสแปม
    for phrase in spam_phrases:
        if phrase in lower_text:
            return None
            
    # 7. กรองการปั๊มตัวเลข (เช่น พิมพ์ตัวเลขเกินครึ่งของข้อความ)
    if sum(c.isdigit() for c in text) > len(text) * 0.5:
        return None

    # 8. ป้องกันคอมเมนต์ซ้ำ (Duplicate)
    if lower_text in seen_comments:
        return None
    seen_comments.add(lower_text)

    return text

# กำหนดชื่อไฟล์ที่ต้องการคลีน
INPUT_FILE = "commentAnilist/clean_comment_anilst.json"
OUTPUT_FILE = "commentAnilist/clean_comment_anilst_final.json"

if os.path.exists(INPUT_FILE):
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = []
    for item in data:
        # ดึงข้อความจากฟิลด์ "text" มาคลีน
        cleaned_text = clean_comment(item.get("text", ""))
        
        if cleaned_text:
            # เก็บข้อมูลเดิมไว้ แต่เปลี่ยนข้อความเป็นอันที่คลีนแล้ว
            new_item = item.copy()
            new_item["text"] = cleaned_text
            cleaned_data.append(new_item)

    # บันทึกไฟล์ที่คลีนแล้ว
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
    print(f"เสร็จสิ้น! กรองข้อมูลเหลือ {len(cleaned_data)} จาก {len(data)} รายการ")
else:
    print(f"ไม่พบไฟล์: {INPUT_FILE}")