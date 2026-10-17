"""Tests for sales_toolkit.ai.llm_client.

These tests never touch the internet. They replace requests.post with a fake
function that returns a response we prepared in advance (a technique called
"mocking"). This keeps the tests fast, free, repeatable, and safe to run in
any environment, including continuous integration servers with no API key.
"""

import json

import pytest
import requests

from sales_toolkit.ai import llm_client
from sales_toolkit.ai.llm_client import (
    AnthropicClient,
    GeminiClient,
    KeywordClient,
    LLMError,
    ScriptedClient,
    get_client,
)


class FakeHTTPResponse:
    """Just enough of a requests.Response for our client code."""

    def __init__(self, status_code, body, headers=None):
        self.status_code = status_code
        self._body = body
        self.text = json.dumps(body)
        self.headers = headers or {}

    def json(self):
        return self._body


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    """Write usage logs to a temporary folder and never really sleep."""
    monkeypatch.setattr(llm_client, "USAGE_LOG", tmp_path / "usage.csv")
    monkeypatch.setattr(llm_client.time, "sleep", lambda seconds: None)


def fake_post(responses, captured):
    """Return a replacement for requests.post that replays `responses`."""

    def _post(url, headers=None, json=None, timeout=None):
        captured.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        return responses.pop(0)

    return _post


def test_gemini_request_and_response_parsing(monkeypatch):
    captured = []
    body = {
        "candidates": [{"content": {"parts": [{"text": "Hello"}, {"text": " there"}]}}],
        "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 3,
                          "thoughtsTokenCount": 5},
        "modelVersion": "gemini-test",
    }
    monkeypatch.setattr(requests, "post", fake_post([FakeHTTPResponse(200, body)], captured))

    reply = GeminiClient("secret-key", "gemini-test").generate("Be brief.", "Hi")

    assert reply.text == "Hello there"
    assert reply.input_tokens == 12
    assert reply.output_tokens == 8  # thinking tokens are billed as output
    sent = captured[0]
    assert sent["headers"]["x-goog-api-key"] == "secret-key"
    assert "secret-key" not in sent["url"]  # the key must not be in the URL
    assert sent["json"]["systemInstruction"]["parts"][0]["text"] == "Be brief."
    assert sent["timeout"] is not None  # a request without a timeout can hang forever


def test_anthropic_request_and_response_parsing(monkeypatch):
    captured = []
    body = {
        "content": [{"type": "text", "text": "Hi!"}],
        "usage": {"input_tokens": 20, "output_tokens": 4},
        "model": "claude-test",
    }
    monkeypatch.setattr(requests, "post", fake_post([FakeHTTPResponse(200, body)], captured))

    reply = AnthropicClient("secret-key", "claude-test").generate("Be brief.", "Hi")

    assert reply.text == "Hi!"
    assert (reply.input_tokens, reply.output_tokens) == (20, 4)
    sent = captured[0]
    assert sent["headers"]["x-api-key"] == "secret-key"
    assert sent["headers"]["anthropic-version"] == "2023-06-01"
    assert sent["json"]["system"] == "Be brief."


def test_rate_limit_is_retried_then_succeeds(monkeypatch):
    captured = []
    ok = {"content": [{"type": "text", "text": "done"}], "usage": {}}
    responses = [FakeHTTPResponse(429, {"error": "slow down"}), FakeHTTPResponse(200, ok)]
    monkeypatch.setattr(requests, "post", fake_post(responses, captured))

    reply = AnthropicClient("k").generate("s", "u")

    assert reply.text == "done"
    assert len(captured) == 2


def test_bad_request_is_not_retried_and_does_not_leak_key(monkeypatch):
    captured = []
    responses = [FakeHTTPResponse(400, {"error": {"message": "invalid model"}})]
    monkeypatch.setattr(requests, "post", fake_post(responses, captured))

    with pytest.raises(LLMError) as error:
        GeminiClient("my-very-secret-key").generate("s", "u")

    assert len(captured) == 1
    assert "invalid model" in str(error.value)
    assert "my-very-secret-key" not in str(error.value)


def test_missing_key_gives_helpful_error(monkeypatch):
    monkeypatch.setattr(llm_client, "load_settings", lambda: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(LLMError, match="GEMINI_API_KEY"):
        get_client("gemini")


def test_keyword_client_works_offline():
    reply = KeywordClient().generate("", "Please send 2 boxes of blue pens and 10% off")
    data = json.loads(reply.text)
    assert data["items"] == [{"sku": "SKU-002", "quantity": 2}]
    assert data["requested_discount_percent"] == 10


def test_scripted_client_records_calls():
    client = ScriptedClient(["first", "second"])
    assert client.generate("sys", "a").text == "first"
    assert client.generate("sys", "b").text == "second"
    assert [call["user_message"] for call in client.calls] == ["a", "b"]
    with pytest.raises(LLMError):
        client.generate("sys", "c")
