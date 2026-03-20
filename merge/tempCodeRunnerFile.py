import json
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Note: If the above import fails, install vaderSentiment: pip install vaderSentiment Error: matplotlib is not installed. Please install it using: pip install matplotlib

# -----------------------------
# 1. โหลดข้อมูล JSON
# -----------------------------
with open("./merge/anime_comments_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# -----------------------------
# 2. สร้าง sentiment analyzer
# -----------------------------


def get_sentiment(text):
    score = analyzer.polarity_scores(text)
    return score["compound"]

# วิเคราะห์ sentiment ของ comment
df["sentiment_score"] = df["comment"].apply(get_sentiment)

# -----------------------------
# 3. แปลงเป็นคะแนน 0-10
# -----------------------------
df["rating"] = (df["sentiment_score"] + 1) * 5

# -----------------------------
# 4. แยก genre (กรณีมีหลาย genre)
# -----------------------------
df["Genres"] = df["Genres"].str.split(",")

df = df.explode("Genres")

df["Genres"] = df["Genres"].str.strip()

# -----------------------------
# 5. คำนวณคะแนนเฉลี่ยตาม Genre
# -----------------------------
genre_scores = df.groupby("Genres")["rating"].mean().sort_values(ascending=False)

print("\nAverage Genre Scores:")
print(genre_scores)

# -----------------------------
# 6. คำนวณคะแนนเฉลี่ยตาม Anime
# -----------------------------
anime_scores = df.groupby("anime_name")["rating"].mean().sort_values(ascending=False)

print("\nAverage Anime Scores:")
print(anime_scores)

# -----------------------------
# 7. วาดกราฟ Genre Score
# -----------------------------
plt.figure(figsize=(12,6))

genre_scores.plot(kind="bar")

plt.title("Average Anime Genre Score from Comments")
plt.xlabel("Genre")
plt.ylabel("Score")

plt.xticks(rotation=45)

plt.ylim(5,7)

for i, v in enumerate(genre_scores):
    plt.text(i, v + 0.02, f"{v:.2f}", ha="center")

plt.tight_layout()

plt.show()