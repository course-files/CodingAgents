"""A small, provider-neutral client for calling a large language model (LLM).

Why this module exists
----------------------
Every model provider (Google, Anthropic, OpenAI, and others) offers the same
basic service: you send some text over HTTPS, and the model sends text back.
The details differ: the web address, the name of the header that carries
your API key, the shape of the JSON you send, and where the answer sits in
the JSON you receive.

This module hides those differences behind ONE simple method:

    response = client.generate(system_prompt, user_message)
    print(response.text)

The rest of the program never needs to know which provider is in use. To
switch provider you change one setting (LLM_PROVIDER in your .env file),
not your code. This is called the "adapter" pattern, and it is the main
reason the ideas in this lab transfer to any model you meet in future.

Providers supported
-------------------
    gemini     Google Gemini API, free tier available (age 18+).
    anthropic  Anthropic Claude API, paid per use.
    keyword    An offline, rule-based stand-in. No network, no key, no cost.
               It is deliberately simple, so you can compare it with a real
               model in Step 20.

There is also ScriptedClient, used only inside automated tests.

Settings are read from environment variables (normally via a .env file):

    LLM_PROVIDER       gemini | anthropic | keyword      (default: keyword)
    GEMINI_API_KEY     your Google AI Studio key          (gemini only)
    GEMINI_MODEL       default: gemini-3.5-flash-lite
    ANTHROPIC_API_KEY  your Claude Console key            (anthropic only)
    ANTHROPIC_MODEL    default: claude-haiku-5-5
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import requests

# ---------------------------------------------------------------------------
# Default settings. Model names change over time; check the provider's
# documentation and override them in .env rather than editing this file.
# ---------------------------------------------------------------------------
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"
DEFAULT_ANTHROPIC_MODEL = "claude-haiku-5-5"

# How long to wait for the server before giving up, in seconds. Without a
# timeout, a request to a slow or unreachable server can hang forever.
REQUEST_TIMEOUT_SECONDS = 60

# HTTP status codes that are usually temporary, so it is worth trying again:
#   429 = too many requests (you hit a rate limit)
#   500, 502, 503, 504 = a problem on the provider's side
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3

# Upper limit on the length of each reply. Some models "think" before they
# answer, and those hidden thinking tokens count towards this limit, so it is
# set generously. You only pay for the tokens actually used.
DEFAULT_MAX_OUTPUT_TOKENS = 4096

# Every real API call is recorded here (tokens, time taken, model), so that
# you can work out cost in Step 24. This folder is listed in .gitignore.
USAGE_LOG = Path("logs") / "llm_usage.csv"


class LLMError(Exception):
    """Raised when a model call fails in a way the caller should handle."""


@dataclass
class LLMResponse:
    """The parts of a model's reply that the rest of the program needs.

    Attributes:
        text:          the model's answer as plain text.
        model:         the model that produced it.
        input_tokens:  tokens you sent (you pay for these).
        output_tokens: tokens the model generated, including any hidden
                       "thinking" tokens (you pay for these too, usually at
                       a higher price than input tokens).
        latency_seconds: how long the call took, end to end.
        raw:           the full JSON response, kept for inspection.
    """

    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_seconds: float = 0.0
    raw: dict = field(default_factory=dict, repr=False)


class BaseClient:
    """What every client must provide: a name and a generate() method."""

    provider = "base"
    model = "none"

    def generate(
        self, system_prompt: str, user_message: str, max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    ) -> LLMResponse:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Shared HTTP logic: send the request, retry temporary failures, time it.
# ---------------------------------------------------------------------------
def _post_with_retries(url: str, headers: dict, payload: dict) -> tuple[dict, float]:
    """POST a JSON payload and return (response JSON, seconds taken).

    Retries temporary failures with "exponential backoff": wait 2 seconds,
    then 4, then 8. If the server sends a Retry-After header, that value is
    used instead, because the server knows best when to try again.
    """
    last_error = "no attempt made"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        try:
            reply = requests.post(
                url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT_SECONDS
            )
        except requests.RequestException as exc:
            # Network problems: no internet, DNS failure, timeout, and so on.
            last_error = f"network error: {exc.__class__.__name__}"
        else:
            elapsed = time.perf_counter() - started
            if reply.status_code == 200:
                return reply.json(), elapsed
            # Never include request headers in an error message: they
            # contain your API key. The response body is safe to show.
            last_error = f"HTTP {reply.status_code}: {reply.text[:500]}"
            if reply.status_code not in RETRYABLE_STATUS_CODES:
                break  # for example 400 (bad request) or 401 (bad key)
            retry_after = reply.headers.get("retry-after")
            if retry_after and retry_after.isdigit():
                time.sleep(min(int(retry_after), 60))
                continue
        if attempt < MAX_ATTEMPTS:
            time.sleep(2**attempt)
    raise LLMError(f"Model call failed after {attempt} attempt(s). Last error: {last_error}")


def _log_usage(response: LLMResponse, provider: str) -> None:
    """Append one row per call to logs/llm_usage.csv."""
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    new_file = not USAGE_LOG.exists()
    with open(USAGE_LOG, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(
                ["timestamp_utc", "provider", "model", "input_tokens",
                 "output_tokens", "latency_seconds"]
            )
        writer.writerow(
            [datetime.now(timezone.utc).isoformat(timespec="seconds"), provider,
             response.model, response.input_tokens, response.output_tokens,
             f"{response.latency_seconds:.2f}"]
        )


# ---------------------------------------------------------------------------
# Google Gemini
# ---------------------------------------------------------------------------
class GeminiClient(BaseClient):
    """Calls the Gemini API "generateContent" endpoint.

    Google also offers a newer "Interactions" API. This lab uses
    generateContent because it is stateless: Google does not keep your
    conversation for later turns. The Interactions API stores requests by
    default unless you send "store": false.
    """

    provider = "gemini"

    def __init__(self, api_key: str, model: str = DEFAULT_GEMINI_MODEL):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt, user_message, max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )
        # The key goes in a header, not in the URL. URLs end up in browser
        # history, proxy logs and error messages; headers usually do not.
        headers = {"x-goog-api-key": self.api_key, "Content-Type": "application/json"}
        payload = {
            # Instructions that apply to the whole conversation.
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            # The conversation itself. One user turn is enough here.
            "contents": [{"role": "user", "parts": [{"text": user_message}]}],
            "generationConfig": {"maxOutputTokens": max_output_tokens},
        }
        data, elapsed = _post_with_retries(url, headers, payload)

        # The answer is at candidates[0].content.parts[*].text
        candidates = data.get("candidates") or []
        if not candidates:
            # This happens, for example, when a safety filter blocks the prompt.
            raise LLMError(f"Gemini returned no answer: {json.dumps(data)[:500]}")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts if not part.get("thought"))

        usage = data.get("usageMetadata", {})
        response = LLMResponse(
            text=text,
            model=data.get("modelVersion", self.model),
            input_tokens=usage.get("promptTokenCount", 0),
            # Thinking tokens are billed as output, so count them here.
            output_tokens=usage.get("candidatesTokenCount", 0)
            + usage.get("thoughtsTokenCount", 0),
            latency_seconds=elapsed,
            raw=data,
        )
        _log_usage(response, self.provider)
        return response


# ---------------------------------------------------------------------------
# Anthropic Claude
# ---------------------------------------------------------------------------
class AnthropicClient(BaseClient):
    """Calls the Anthropic Messages API (paid, billed through the Claude Console).

    Note: a Claude Pro subscription does NOT include API usage. The API is
    billed separately in the Claude Console.
    """

    provider = "anthropic"

    def __init__(self, api_key: str, model: str = DEFAULT_ANTHROPIC_MODEL):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt, user_message, max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",  # the API version, not a date you change
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_output_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        data, elapsed = _post_with_retries(url, headers, payload)

        # The answer is a list of content blocks; keep the text blocks.
        text = "".join(
            block.get("text", "") for block in data.get("content", [])
            if block.get("type") == "text"
        )
        usage = data.get("usage", {})
        response = LLMResponse(
            text=text,
            model=data.get("model", self.model),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            latency_seconds=elapsed,
            raw=data,
        )
        _log_usage(response, self.provider)
        return response


# ---------------------------------------------------------------------------
# Offline clients (no network, no key, no cost)
# ---------------------------------------------------------------------------
class KeywordClient(BaseClient):
    """A rule-based stand-in for a model, for offline work.

    It looks for catalogue keywords and the number just before them. It
    knows nothing about Kiswahili, corrections ("actually make that three"),
    or context. That is the point: in Step 20 you measure how far simple
    rules get you, and in Step 22 you compare a real model against it.

    It returns JSON in the same shape the real model is asked to produce,
    so the rest of the program cannot tell the difference.
    """

    provider = "keyword"
    model = "keyword-rules-v1"

    # keyword -> SKU. Deliberately incomplete.
    KEYWORDS = {
        "exercise book": "SKU-001", "pen": "SKU-002", "flash drive": "SKU-003",
        "mouse": "SKU-004", "water": "SKU-005", "coffee": "SKU-006",
        "paper": "SKU-007", "hdmi": "SKU-008", "highlighter": "SKU-009",
        "stapler": "SKU-010", "sugar": "SKU-011", "charger": "SKU-012",
    }
    NUMBER_WORDS = {
        "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "dozen": 12,
    }

    def generate(self, system_prompt, user_message, max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        started = time.perf_counter()
        lowered = user_message.lower()
        items = []
        for keyword, sku in self.KEYWORDS.items():
            found = re.search(r"\b" + re.escape(keyword), lowered)
            if not found:
                continue
            # Look at up to four words before the keyword for a quantity,
            # for example "2 boxes of blue pens" or "a dozen exercise books".
            words_before = re.findall(r"[a-z0-9]+", lowered[: found.start()])[-4:]
            quantity = 1
            for word in reversed(words_before):
                if word.isdigit():
                    quantity = int(word)
                    break
                if word in self.NUMBER_WORDS:
                    quantity = self.NUMBER_WORDS[word]
                    break
            items.append({"sku": sku, "quantity": quantity})
        discount = re.search(r"(\d+)\s*%", lowered)
        answer = {
            "items": items,
            "unmatched": [],
            "requested_discount_percent": int(discount.group(1)) if discount else None,
            "needs_review": False,
        }
        return LLMResponse(
            text=json.dumps(answer), model=self.model,
            latency_seconds=time.perf_counter() - started,
        )


class ScriptedClient(BaseClient):
    """A fake client for automated tests.

    You decide in advance what it "replies". It records every call, so a
    test can check what your code sent. Tests that use it run instantly,
    offline and free, and give the same result every time, which a real
    model cannot promise.

    Example:
        client = ScriptedClient(['{"items": [], "unmatched": [], '
                                 '"requested_discount_percent": null, '
                                 '"needs_review": false}'])
        order = parse_order("Hello", catalogue, client)
        assert client.calls[0]["user_message"] == "Hello"
    """

    provider = "scripted"
    model = "scripted"

    def __init__(self, replies: list[str] | Callable[[str, str], str]):
        self.replies = replies
        self.calls: list[dict] = []

    def generate(self, system_prompt, user_message, max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        self.calls.append({"system_prompt": system_prompt, "user_message": user_message})
        if callable(self.replies):
            text = self.replies(system_prompt, user_message)
        else:
            if len(self.calls) > len(self.replies):
                raise LLMError("ScriptedClient ran out of scripted replies")
            text = self.replies[len(self.calls) - 1]
        return LLMResponse(text=text, model=self.model)


# ---------------------------------------------------------------------------
# Choosing a client from settings
# ---------------------------------------------------------------------------
def load_settings() -> None:
    """Load variables from a .env file in the current folder, if present.

    Real environment variables take priority over the .env file.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:  # python-dotenv not installed; rely on real env vars
        return
    load_dotenv(override=False)


def get_client(provider: str | None = None) -> BaseClient:
    """Return a client for the configured provider.

    Raises LLMError with a helpful message if a key is missing.
    """
    load_settings()
    provider = (provider or os.getenv("LLM_PROVIDER") or "keyword").strip().lower()

    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY", "").strip()
        if not key:
            raise LLMError("GEMINI_API_KEY is not set. See Step 16 of the lab.")
        return GeminiClient(key, os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL)

    if provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not key:
            raise LLMError("ANTHROPIC_API_KEY is not set. See Step 16 of the lab.")
        return AnthropicClient(key, os.getenv("ANTHROPIC_MODEL") or DEFAULT_ANTHROPIC_MODEL)

    if provider == "keyword":
        return KeywordClient()

    raise LLMError(
        f"Unknown LLM_PROVIDER '{provider}'. Use gemini, anthropic or keyword."
    )
