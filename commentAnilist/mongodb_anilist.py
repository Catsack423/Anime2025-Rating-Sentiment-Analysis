from pymongo import MongoClient
import json

file_path = "anime_2024_2025_thread_comments.json"

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    data = None
except json.JSONDecodeError:
    print("Invalid JSON format")
    data = None

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Dataen"]
    collection = db["Anilist"]

    # แก้ไขจุดนี้: rows เป็น list อยู่แล้ว ใช้ได้เลย
    if data:
        result = collection.insert_many(data)
        print(f":white_check_mark: Success! Inserted {len(result.inserted_ids)} anime records.")
    else:
        print(":warning: No data found to insert.")
        
except Exception as e:
    print(f":x: An error occurred: {e}")
finally:
    client.close()