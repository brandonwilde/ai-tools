"""Tests for Anthropic prompt-caching support in anthropic_tools.py."""
import os
import sys
import types

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aitools.third_party_apis import anthropic_tools  # noqa: E402


class FakeUsage:
    def __init__(self, input_tokens=10, output_tokens=5,
                 cache_creation_input_tokens=None, cache_read_input_tokens=None):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        # Only set these attrs when provided, to simulate older SDKs / responses
        # that omit them entirely (getattr fallback path).
        if cache_creation_input_tokens is not None:
            self.cache_creation_input_tokens = cache_creation_input_tokens
        if cache_read_input_tokens is not None:
            self.cache_read_input_tokens = cache_read_input_tokens


class FakeTextBlock:
    type = "text"

    def __init__(self, text):
        self.text = text


class FakeMessage:
    def __init__(self, text="hello", usage=None):
        self.content = [FakeTextBlock(text)]
        self.usage = usage or FakeUsage()


class FakeMessagesResource:
    def __init__(self, response=None):
        self.response = response or FakeMessage()
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return self.response


class FakeClient:
    def __init__(self, response=None):
        self.messages = FakeMessagesResource(response=response)


def _patch_client(monkeypatch, response=None):
    fake_client = FakeClient(response=response)
    monkeypatch.setattr(anthropic_tools, "_get_client", lambda: fake_client)
    return fake_client


def test_cache_system_prompt_true_adds_single_breakpoint(monkeypatch):
    fake_client = _patch_client(monkeypatch)

    anthropic_tools.prompt_claude(
        messages=[{"text": "hi"}],
        system_prompt=["You are a helpful assistant.", "Be terse."],
        cache_system_prompt=True,
    )

    system_blocks = fake_client.messages.last_kwargs["system"]
    cache_controlled = [b for b in system_blocks if "cache_control" in b]
    assert len(cache_controlled) == 1
    assert cache_controlled[0] is system_blocks[-1]
    assert cache_controlled[0]["cache_control"] == {"type": "ephemeral"}


def test_cache_system_prompt_false_adds_no_breakpoint(monkeypatch):
    fake_client = _patch_client(monkeypatch)

    anthropic_tools.prompt_claude(
        messages=[{"text": "hi"}],
        system_prompt=["You are a helpful assistant.", "Be terse."],
        cache_system_prompt=False,
    )

    system_blocks = fake_client.messages.last_kwargs["system"]
    assert all("cache_control" not in b for b in system_blocks)


def test_per_message_cache_marker_still_works(monkeypatch):
    fake_client = _patch_client(monkeypatch)

    anthropic_tools.prompt_claude(
        messages=[
            {"text": "first turn"},
            {"text": "latest turn", "cache": True},
        ],
        cache_system_prompt=False,
    )

    messages = fake_client.messages.last_kwargs["messages"]
    content = messages[0]["content"]
    # Only the block marked with "cache": True should carry a breakpoint.
    assert "cache_control" not in content[0]
    assert content[1]["cache_control"] == {"type": "ephemeral"}


def test_cache_tokens_surfaced_from_usage(monkeypatch):
    usage = FakeUsage(input_tokens=100, output_tokens=20,
                       cache_creation_input_tokens=50, cache_read_input_tokens=200)
    _patch_client(monkeypatch, response=FakeMessage(usage=usage))

    result = anthropic_tools.prompt_claude(messages=[{"text": "hi"}])

    assert result["input_tokens"] == 100
    assert result["output_tokens"] == 20
    assert result["cache_write_tokens"] == 50
    assert result["cache_read_tokens"] == 200


def test_cache_tokens_default_to_zero_when_absent(monkeypatch):
    # Simulate an older SDK / response with no cache fields on usage at all.
    usage = FakeUsage(input_tokens=100, output_tokens=20)
    _patch_client(monkeypatch, response=FakeMessage(usage=usage))

    result = anthropic_tools.prompt_claude(messages=[{"text": "hi"}])

    assert result["cache_write_tokens"] == 0
    assert result["cache_read_tokens"] == 0
