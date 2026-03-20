import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

analyzer = SentimentIntensityAnalyzer()

with open("commentYoutube/anime_comments_cleaned_promax.json", "r", encoding="utf-8") as f:
    comments = json.load(f)

anime_scores = {}
anime_counts = {}

results = []

for c in comments:

    text = c["comment_text"]
    anime = c["anime_name"]

    score = analyzer.polarity_scores(text)
    compound = score["compound"]

    results.append({
        "anime_name": anime,
        "comment": text,
        "sentiment_score": compound
    })

    if anime not in anime_scores:
        anime_scores[anime] = 0
        anime_counts[anime] = 0

    anime_scores[anime] += compound
    anime_counts[anime] += 1


anime_avg = {}

for anime in anime_scores:
    avg = anime_scores[anime] / anime_counts[anime]

    score10 = (avg + 1) * 5

    anime_avg[anime] = round(score10,2)


with open("anime_rating_results.json", "w", encoding="utf-8") as f:
    json.dump(anime_avg, f, ensure_ascii=False, indent=2)


print("Anime Rating:")

for a in anime_avg:
    print(a, ":", anime_avg[a], "/10")

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