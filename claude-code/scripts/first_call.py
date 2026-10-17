"""Step 17: your first network call to a frontier AI model.

This script deliberately does NOT use sales_toolkit.ai.llm_client. It builds
the HTTP request by hand, so that you can see every part of it: the web
address, the headers, the JSON body, and the JSON that comes back.

Run it from the track folder, with your virtual environment active:

    python scripts/first_call.py
    python scripts/first_call.py "Explain what an invoice is in one sentence."

It uses LLM_PROVIDER, GEMINI_API_KEY / ANTHROPIC_API_KEY and the model
settings from your .env file (see .env.example).
"""

from __future__ import annotations

import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

# 1. Read settings from .env. The key is NEVER written in this file.
load_dotenv()
provider = os.getenv("LLM_PROVIDER", "").strip().lower()
prompt = sys.argv[1] if len(sys.argv) > 1 else "In one sentence, what is a VAT invoice?"


def masked(key: str) -> str:
    """Show only the last 4 characters of a secret, e.g. '...a1b2'."""
    return "..." + key[-4:] if len(key) > 8 else "(too short; check your key)"


# 2. Build the request. Compare the two providers: same idea, different shape.
if provider == "gemini":
    key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL") or "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
elif provider == "anthropic":
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    model = os.getenv("ANTHROPIC_MODEL") or "claude-haiku-5-5"
    url = "https://api.anthropic.com/v1/messages"
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    body = {"model": model, "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}]}
else:
    sys.exit("Set LLM_PROVIDER to gemini or anthropic in your .env file (Step 16).")

if not key:
    sys.exit(f"No API key found for {provider}. Check your .env file (Step 16).")

print("=== REQUEST ===")
print("POST", url)
print("Headers:", {k: (masked(v) if "key" in k.lower() else v) for k, v in headers.items()})
print("Body:", json.dumps(body, indent=2))

# 3. Send it and time it. The timeout stops the program hanging forever.
started = time.perf_counter()
try:
    reply = requests.post(url, headers=headers, json=body, timeout=60)
except requests.RequestException as exc:
    sys.exit(f"Network problem: {exc.__class__.__name__}. Check your internet connection.")
seconds = time.perf_counter() - started

print("\n=== RESPONSE ===")
print("HTTP status:", reply.status_code, f"(took {seconds:.2f} seconds)")
try:
    data = reply.json()
except ValueError:  # the server did not send JSON (rare, but possible)
    data = {}
print(json.dumps(data, indent=2)[:3000] if data else reply.text[:3000])

if reply.status_code != 200:
    sys.exit("\nThe call failed. Read the error message above; Step 17 explains common causes.")

# 4. Pull out the parts that matter. Notice WHERE each provider puts them.
if provider == "gemini":
    parts = data["candidates"][0]["content"]["parts"]
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    usage = data.get("usageMetadata", {})
    tokens_in = usage.get("promptTokenCount", 0)
    tokens_out = usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0)
else:
    text = "".join(b.get("text", "") for b in data["content"] if b.get("type") == "text")
    tokens_in = data["usage"]["input_tokens"]
    tokens_out = data["usage"]["output_tokens"]

print("\n=== WHAT YOUR PROGRAM ACTUALLY NEEDS ===")
print("Answer:       ", text.strip())
print("Input tokens: ", tokens_in)
print("Output tokens:", tokens_out, "(includes any hidden thinking tokens)")
print(f"Latency:       {seconds:.2f} s")
