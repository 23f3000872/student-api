from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from textblob import TextBlob
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

    results = []

    for sentence in req.sentences:
        polarity = TextBlob(sentence).sentiment.polarity

        if polarity > 0.1:
            sentiment = "happy"
        elif polarity < -0.1:
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