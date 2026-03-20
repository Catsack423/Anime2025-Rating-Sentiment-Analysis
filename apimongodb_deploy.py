from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List, Optional

app = FastAPI(title="Anime List API")

client = MongoClient("mongodb://localhost:27017/")
db = client["Dataen"]
collection = db["AnimeList"]
collection_Anilist = db["Anilist"]
collection_youtube = db["youtube"]
collection_cAnimelist = db["comment_animelist"]

@app.get("/")
def read_root():
    return {"message": "Welcome to Anime List API"}

@app.get("/anime", response_model=List[dict])
def get_all_anime():
    animes = list(collection.find({}, {"_id": 0}))
    return animes

@app.get("/Anilist", response_model=List[dict])
def get_all_anime():
    animes = list(collection_Anilist.find({}, {"_id": 0}))
    return animes

@app.get("/youtube", response_model=List[dict])
def get_all_anime():
    animes = list(collection_youtube.find({}, {"_id": 0}))
    return animes

@app.get("/Animelist", response_model=List[dict])
def get_all_anime():
    animes = list(collection_cAnimelist.find({}, {"_id": 0}))
    return animes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9919)