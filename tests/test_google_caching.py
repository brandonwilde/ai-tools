"""Tests for Gemini cache-token mapping in google_tools.py."""
import os
import sys

os.environ.setdefault("GOOGLE_API_KEY", "test-key")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aitools.third_party_apis import google_tools  # noqa: E402


class FakeUsageMetadata:
    def __init__(self, prompt_token_count, candidates_token_count, cached_content_token_count=None):
        self.prompt_token_count = prompt_token_count
        self.candidates_token_count = candidates_token_count
        if cached_content_token_count is not None:
            self.cached_content_token_count = cached_content_token_count


class FakeResponse:
    def __init__(self, text, usage_metadata):
        self.text = text
        self.usage_metadata = usage_metadata


class FakeGenerativeModel:
    def __init__(self, response):
        self._response = response

    def generate_content(self, **kwargs):
        return self._response


def _patch_model(monkeypatch, response):
    monkeypatch.setattr(
        google_tools.genai,
        "GenerativeModel",
        lambda **kwargs: FakeGenerativeModel(response),
    )


def test_gemini_subtracts_cached_tokens_from_input(monkeypatch):
    # prompt_token_count includes cached_content_token_count (per Gemini docs),
    # so input_tokens must be the difference to avoid double-billing cached tokens.
    usage = FakeUsageMetadata(
        prompt_token_count=1000,
        candidates_token_count=50,
        cached_content_token_count=600,
    )
    _patch_model(monkeypatch, FakeResponse("hi", usage))

    result = google_tools.prompt_gemini(messages=[{"text": "hi"}])

    assert result["input_tokens"] == 400
    assert result["cache_read_tokens"] == 600
    assert result["output_tokens"] == 50


def test_gemini_falls_back_when_no_cache_fields(monkeypatch):
    usage = FakeUsageMetadata(prompt_token_count=1000, candidates_token_count=50)
    _patch_model(monkeypatch, FakeResponse("hi", usage))

    result = google_tools.prompt_gemini(messages=[{"text": "hi"}])

    assert result["input_tokens"] == 1000
    assert result["cache_read_tokens"] == 0
    assert result["output_tokens"] == 50
