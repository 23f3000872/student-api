from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Student API
# -------------------------

df = pd.read_csv("q-fastapi.csv")

@app.get("/")
def root():
    return {"message": "Student API Running"}

@app.get("/api")
def get_students(class_: list[str] | None = Query(None, alias="class")):
    data = df

    if class_:
        data = data[data["class"].isin(class_)]

    return {
        "students": data.to_dict(orient="records")
    }

# -------------------------
# Sentiment API
# -------------------------

class SentimentRequest(BaseModel):
    sentences: List[str]

@app.post("/sentiment")
def sentiment(req: SentimentRequest):

    happy_words = {
        "love", "great", "awesome", "excellent", "good",
        "happy", "amazing", "wonderful", "fantastic", "like",
        "best", "beautiful", "nice", "enjoy", "thrilled",
        "excited", "positive", "outstanding", "perfect",
        "brilliant", "superb", "delightful", "pleased",
        "joy", "joyful", "glad", "success", "successful",
        "win", "winning", "loved", "liked"
    }

    sad_words = {
        "sad", "terrible", "bad", "hate", "awful",
        "horrible", "worst", "angry", "disappointed",
        "upset", "poor", "boring", "miserable",
        "negative", "failure", "failed", "loser",
        "losing", "depressed", "unhappy", "regret",
        "regrettable", "disaster", "annoying",
        "frustrated", "frustrating", "pathetic",
        "useless", "disappointing", "hated"
    }

    results = []

    for sentence in req.sentences:
        text = sentence.lower()

        happy_score = sum(
            1 for word in happy_words if word in text
        )

        sad_score = sum(
            1 for word in sad_words if word in text
        )

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