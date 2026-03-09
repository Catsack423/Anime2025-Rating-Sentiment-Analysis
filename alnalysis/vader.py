import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# โหลดโมเดล sentiment
analyzer = SentimentIntensityAnalyzer()

# อ่านไฟล์คอมเมนต์
with open("commentYoutube/anime_comments_cleaned_promax.json", "r", encoding="utf-8") as f:
    comments = json.load(f)

anime_scores = {}
anime_counts = {}

results = []

for c in comments:

    text = c["comment_text"]
    anime = c["anime_name"]

    # วิเคราะห์ sentiment
    score = analyzer.polarity_scores(text)
    compound = score["compound"]

    # เก็บผลลัพธ์
    results.append({
        "anime_name": anime,
        "comment": text,
        "sentiment_score": compound
    })

    # รวมคะแนนต่อ anime
    if anime not in anime_scores:
        anime_scores[anime] = 0
        anime_counts[anime] = 0

    anime_scores[anime] += compound
    anime_counts[anime] += 1


# คำนวณค่าเฉลี่ย sentiment
anime_avg = {}

for anime in anime_scores:
    avg = anime_scores[anime] / anime_counts[anime]

    # แปลงเป็นคะแนน 0-10
    score10 = (avg + 1) * 5

    anime_avg[anime] = round(score10,2)


# บันทึกผลลัพธ์
with open("anime_rating_results.json", "w", encoding="utf-8") as f:
    json.dump(anime_avg, f, ensure_ascii=False, indent=2)


print("Anime Rating:")

for a in anime_avg:
    print(a, ":", anime_avg[a], "/10")


# ----------- ทำกราฟ -----------

names = list(anime_avg.keys())
scores = list(anime_avg.values())

plt.figure(figsize=(10,5))
plt.bar(names, scores)

plt.title("Anime Rating Based on YouTube Comments")
plt.xlabel("Anime")
plt.ylabel("Score (0-10)")
plt.xticks(rotation=45)

for i,v in enumerate(scores):
    plt.text(i, v+0.1, str(v), ha="center")

plt.show()