"""Tests for DeepSeek cache-token mapping in deepseek_tools.py."""
import os
import sys

os.environ.setdefault("DEEPSEEK_API_KEY", "test-key")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aitools.third_party_apis import deepseek_tools  # noqa: E402


class FakeUsage:
    def __init__(self, prompt_tokens, completion_tokens,
                 prompt_cache_hit_tokens=None, prompt_cache_miss_tokens=None):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        if prompt_cache_hit_tokens is not None:
            self.prompt_cache_hit_tokens = prompt_cache_hit_tokens
        if prompt_cache_miss_tokens is not None:
            self.prompt_cache_miss_tokens = prompt_cache_miss_tokens


class FakeMessage:
    def __init__(self, content="hi"):
        self.content = content


class FakeChoice:
    def __init__(self, content="hi"):
        self.message = FakeMessage(content)


class FakeChatResponse:
    def __init__(self, usage, content="hi"):
        self.choices = [FakeChoice(content)]
        self.usage = usage


class FakeCompletions:
    def __init__(self, response):
        self.response = response

    def create(self, **kwargs):
        return self.response


class FakeChat:
    def __init__(self, response):
        self.completions = FakeCompletions(response)


class FakeClient:
    def __init__(self, response):
        self.chat = FakeChat(response)


def _patch_client(monkeypatch, response):
    fake_client = FakeClient(response)
    monkeypatch.setattr(deepseek_tools, "_get_client", lambda: fake_client)
    return fake_client


def test_deepseek_maps_cache_hit_and_miss_tokens(monkeypatch):
    usage = FakeUsage(
        prompt_tokens=1000,
        completion_tokens=50,
        prompt_cache_hit_tokens=700,
        prompt_cache_miss_tokens=300,
    )
    _patch_client(monkeypatch, FakeChatResponse(usage))

    result = deepseek_tools.prompt_deepseek(messages=[{"text": "hi"}])

    # input_tokens should be cache_miss only, not the full prompt_tokens
    # (which includes the cache hits) -- otherwise cached tokens get billed twice.
    assert result["input_tokens"] == 300
    assert result["cache_read_tokens"] == 700
    assert result["output_tokens"] == 50


def test_deepseek_falls_back_when_cache_fields_absent(monkeypatch):
    usage = FakeUsage(prompt_tokens=1000, completion_tokens=50)
    _patch_client(monkeypatch, FakeChatResponse(usage))

    result = deepseek_tools.prompt_deepseek(messages=[{"text": "hi"}])

    assert result["input_tokens"] == 1000
    assert result["output_tokens"] == 50
    assert "cache_read_tokens" not in result
