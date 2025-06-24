# summarizer.py

# Text Summarization Script using Hugging Face Transformers

# This script allows users to input any article or long text and get a concise summary using a pre-trained NLP model.
# Code

from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_text(article):
    summary = summarizer(article, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    print("Initializing the summarization model...")
    article = input("Please paste the text you want to summarize:\n\n")
    print("\nGenerating summary...\n")
    summary = summarize_text(article)
    print("Summary:")
    print(summary)
