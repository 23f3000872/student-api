from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from typing import List

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
        "love", "great", "awesome", "excellent", "good",
        "happy", "amazing", "wonderful", "fantastic", "like",
        "best", "beautiful", "nice", "enjoy"
    }

    sad_words = {
        "sad", "terrible", "bad", "hate", "awful",
        "horrible", "worst", "angry", "disappointed",
        "upset", "poor", "boring"
    }

    results = []

    for sentence in req.sentences:
        text = sentence.lower()

        if any(word in text for word in happy_words):
            sentiment = "happy"
        elif any(word in text for word in sad_words):
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