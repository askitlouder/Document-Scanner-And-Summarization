import os
import time
from typing import List
import logging
from dotenv import load_dotenv

load_dotenv() #It use to fetch the env variables from .env file

# Use the google genai client
try:
    from google import genai
except Exception:
    # Newer SDK uses "google.genai" or "google" package. User should install the appropriate package.
    raise

DEFAULT_MODEL = "gemini-2.5-flash-lite"   # configurable; update if you have a different model

def make_client():
    # The genai client picks up application default credentials by default.
    try:
        client = genai.Client(api_key = os.getenv('GOOGLE_GEMINI_API_KEY'))
    except Exception as e:
        print("Failed creating genai client. Ensure GOOGLE_APPLICATION_CREDENTIALS is set and vertex ai enabled.")
        raise
    return client

def chunk_text(text: str, max_chars: int = 3000):
    """
    Simple chunker to break long text into manageable lengths for the model.
    Adjust max_chars according to model/context limits.
    """
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        # attempt to split on nearest newline or sentence end
        slice_ = text[start:end]
        # try to find last double newline
        pivot = slice_.rfind('\n\n')
        if pivot == -1:
            pivot = slice_.rfind('. ')
        if pivot == -1:
            pivot = end
        else:
            pivot = start + pivot + 1
        chunks.append(text[start:pivot].strip())
        start = pivot
    return chunks

def summarize_with_gemini(text: str,
                          model: str = DEFAULT_MODEL) -> str:
    if not text or text.strip() == "":
        return ""

    client = make_client()
    chunks = chunk_text(text, max_chars=3000)
    print("Text split into %d chunks for summarization.", len(chunks))

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        prompt = (
            "You are a helpful summarization assistant. "
            "Summarize the following document chunk into concise bullet points and a 2–5 sentence summary. "
            "Preserve any headings found. Output JSON with keys: 'summary' and 'bullets'.\n\n"
            f"DOCUMENT CHUNK:\n{chunk}\n\n"
            "Respond only in JSON."
        )
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            out_text = getattr(response, "text", None)
            if out_text is None:
                # fallback parse
                out_text = str(response)
            chunk_summaries.append(out_text)
        except Exception as e:
            print("Gemini summarization failed for chunk %d", i)
            chunk_summaries.append("")

    # Combine chunk summaries into a final summary prompt
    combined = "\n\n".join(chunk_summaries)
    final_prompt = (
        "You are a helpful summarization assistant. Combine the following chunk summaries into:\n"
        "1) a 4-6 sentence concise summary, and\n"
        "2) a combined ordered list of key bullet points (max 12 bullets).\n\n"
        f"CHUNK_SUMMARIES:\n{combined}\n\nRespond in plain text."
    )
    try:
        final_resp = client.models.generate_content(
            model=model,
            contents=final_prompt
        )
        final_text = getattr(final_resp, "text", None)
        if final_text is None:
            final_text = str(final_resp)
    except ZeroDivisionError as e:
        print("Gemini final summarization failed.")
        final_text = combined  # fallback
    return final_text
