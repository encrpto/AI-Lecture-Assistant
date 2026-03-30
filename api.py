from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import shutil
import os

from pipeline import run_pipeline, answer_question

app = FastAPI()

os.makedirs("data", exist_ok=True)

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/process")
async def process(file: UploadFile):
    with open("data/lecture.mp4", "wb") as f:
        shutil.copyfileobj(file.file, f)

    run_pipeline()

    return {"status": "processed"}

@app.post("/chat")
def chat(q: Query):
    answer = answer_question(q.question)
    return {"answer": answer}