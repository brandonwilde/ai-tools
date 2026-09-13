"""Tests for the shared OpenAI-compatible request helper."""
import os
import sys

os.environ.setdefault("MOONSHOT_API_KEY", "test-key")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

from aitools.third_party_apis import moonshot_tools, openai_compatible  # noqa: E402


class FakeUsage:
    def __init__(self, prompt_tokens, completion_tokens, **cache_fields):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        for name, value in cache_fields.items():
            setattr(self, name, value)


class FakePromptTokensDetails:
    def __init__(self, cached_tokens):
        self.cached_tokens = cached_tokens


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
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return self.response


class FakeChat:
    def __init__(self, response):
        self.completions = FakeCompletions(response)


class FakeClient:
    def __init__(self, response):
        self.chat = FakeChat(response)


def test_deepseek_style_hit_miss_split():
    usage = FakeUsage(
        prompt_tokens=1000,
        completion_tokens=50,
        prompt_cache_hit_tokens=700,
        prompt_cache_miss_tokens=300,
    )
    assert openai_compatible.extract_usage(usage) == {
        "input_tokens": 300,
        "cache_read_tokens": 700,
        "output_tokens": 50,
    }


def test_moonshot_style_top_level_cached_tokens():
    """Moonshot counts cached tokens inside prompt_tokens, so they're subtracted out."""
    usage = FakeUsage(prompt_tokens=1000, completion_tokens=50, cached_tokens=700)
    assert openai_compatible.extract_usage(usage) == {
        "input_tokens": 300,
        "cache_read_tokens": 700,
        "output_tokens": 50,
    }


def test_openai_style_nested_cached_tokens():
    usage = FakeUsage(
        prompt_tokens=1000,
        completion_tokens=50,
        prompt_tokens_details=FakePromptTokensDetails(700),
    )
    assert openai_compatible.extract_usage(usage) == {
        "input_tokens": 300,
        "cache_read_tokens": 700,
        "output_tokens": 50,
    }


def test_no_cache_fields_falls_back_to_prompt_tokens():
    usage = FakeUsage(prompt_tokens=1000, completion_tokens=50)
    result = openai_compatible.extract_usage(usage)

    assert result == {"input_tokens": 1000, "output_tokens": 50}
    assert "cache_read_tokens" not in result


def test_zero_cached_tokens_is_treated_as_no_cache_hit():
    usage = FakeUsage(prompt_tokens=1000, completion_tokens=50, cached_tokens=0)
    result = openai_compatible.extract_usage(usage)

    assert result == {"input_tokens": 1000, "output_tokens": 50}
    assert "cache_read_tokens" not in result


def test_cached_tokens_exceeding_prompt_tokens_does_not_go_negative():
    """Guards a provider that reports the two counts exclusively rather than inclusively."""
    usage = FakeUsage(prompt_tokens=300, completion_tokens=50, cached_tokens=700)
    assert openai_compatible.extract_usage(usage)["input_tokens"] == 0


def test_kimi_omits_temperature_and_uses_max_completion_tokens(monkeypatch):
    usage = FakeUsage(prompt_tokens=1000, completion_tokens=50, cached_tokens=700)
    fake_client = FakeClient(FakeChatResponse(usage))
    monkeypatch.setattr(moonshot_tools, "_get_client", lambda: fake_client)

    result = moonshot_tools.prompt_kimi(messages=[{"text": "hi"}], temperature=0.7)

    sent = fake_client.chat.completions.last_kwargs
    # Kimi fixes its sampling params and errors on an explicit temperature.
    assert "temperature" not in sent
    assert sent["max_completion_tokens"] == 8192
    assert "max_tokens" not in sent
    assert result["cache_read_tokens"] == 700


def test_missing_api_key_raises_before_any_request(monkeypatch):
    monkeypatch.delenv("FAKE_PROVIDER_KEY", raising=False)
    get_client = openai_compatible.make_client_getter("FAKE_PROVIDER_KEY", "https://example.invalid")

    with pytest.raises(ValueError, match="FAKE_PROVIDER_KEY"):
        get_client()
