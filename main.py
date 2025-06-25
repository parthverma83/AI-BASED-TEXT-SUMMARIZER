from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

# Load summarization pipeline
summarizer = pipeline("summarization")

# FastAPI instance
app = FastAPI(title="Text Summarization API")

# Request body model
class Article(BaseModel):
    text: str

# POST endpoint to summarize text
@app.post("/summarize")
async def summarize(article: Article):
    summary = summarizer(
        article.text,
        max_length=130,
        min_length=30,
        do_sample=False
    )
    return {"summary": summary[0]["summary_text"]}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Text Summarization API!"}

# Run with python main.py
if _name_ == "_main_":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)