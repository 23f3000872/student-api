from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("q-fastapi.csv")

@app.get("/api")
def get_students(class_: list[str] | None = Query(None, alias="class")):
    data = df

    if class_:
        data = data[data["class"].isin(class_)]

    return {
        "students": data.to_dict(orient="records")
    }

@app.get("/")
def root():
    return {"message": "Student API Running"}

class SentimentRequest(BaseModel):
    sentences: List[str]

@app.post("/sentiment")
def sentiment(req: SentimentRequest):

    happy_words = {
        "love","great","awesome","excellent","good","happy",
        "amazing","wonderful","fantastic","like","best",
        "beautiful","nice","enjoy","thrilled","excited",
        "positive","outstanding","perfect","brilliant",
        "superb","delightful","pleased","joy","joyful",
        "glad","success","successful","win","winning",
        "smile","cheerful","satisfied","favorite","favourite",
        "incredible","remarkable","thankful","grateful",
        "loved","lovely","adore","adored","celebrate"
    }

    sad_words = {
        "sad","terrible","bad","hate","awful","horrible",
        "worst","angry","disappointed","upset","poor",
        "boring","miserable","negative","failure","failed",
        "loser","losing","depressed","unhappy","regret",
        "regrettable","disaster","annoying","frustrated",
        "frustrating","pathetic","useless","disappointing",
        "cry","crying","hurt","pain","painful","tragic",
        "unfortunate","sucks","suck","fear","worried",
        "anxious","stress","stressed","lonely","broken"
    }

    results = []

    for sentence in req.sentences:
        text = re.sub(r'[^a-zA-Z ]', ' ', sentence.lower())
        words = set(text.split())

        happy_score = len(words & happy_words)
        sad_score = len(words & sad_words)

        if happy_score > sad_score:
            sentiment = "happy"
        elif sad_score > happy_score:
            sentiment = "sad"
        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)