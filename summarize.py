# bot/summarize.py

import re
import logging
from transformers import pipeline

# suppress HuggingFace tokenizer warnings
logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

# Translation (if needed)—keep your existing Cyrillic → English code here,
# or omit it if everything is already in English.

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_text(text: str) -> str:
    """
    Summarize the given text, choosing min/max lengths
    based on the input length so you won’t get warnings.
    """
    # 1) (Optional) detect & translate non-Latin scripts here...

    # 2) Choose summary length dynamically
    words = text.split()
    # aim for roughly 30% of the original word count
    target = max(20, int(len(words) * 0.3))
    min_len = max(5, target // 2)
    max_len = min(150, target * 2)

    out = summarizer(
        text,
        max_length=max_len,
        min_length=min_len,
        truncation=True
    )
    return out[0]["summary_text"].strip()
