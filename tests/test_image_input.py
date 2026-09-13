"""Tests for image media-type detection and the text-only model guard."""
import base64
import os
import sys

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

from aitools.media_tools import text_tools  # noqa: E402
from aitools.media_tools.utils import image_media_type  # noqa: E402
from aitools.third_party_apis.anthropic_tools import format_claude_messages  # noqa: E402
from aitools.third_party_apis.openai_tools import format_openai_messages  # noqa: E402

# Smallest valid PNG, so the formatters have real bytes to encode.
PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


@pytest.fixture
def png_path(tmp_path):
    path = tmp_path / "chart.png"
    path.write_bytes(PNG_BYTES)
    return str(path)


@pytest.mark.parametrize("filename,expected", [
    ("a.png", "image/png"),
    ("a.gif", "image/gif"),
    ("a.webp", "image/webp"),
    ("a.jpeg", "image/jpeg"),
    ("a.jpg", "image/jpeg"),   # normalized to the IANA name
    ("a.PNG", "image/png"),    # extension case is irrelevant
])
def test_image_media_type_maps_extensions(filename, expected):
    assert image_media_type(filename) == expected


def test_image_media_type_rejects_unsupported_extension():
    with pytest.raises(AssertionError, match="PNG, JPEG, GIF, or WEBP"):
        image_media_type("scan.bmp")


def test_openai_formatter_uses_the_real_media_type(png_path):
    """A PNG was previously labelled image/jpeg in the data URI regardless of extension."""
    formatted = format_openai_messages([{"image": png_path}])

    url = formatted[0]["content"][0]["image_url"]["url"]
    assert url.startswith("data:image/png;base64,")


def test_claude_formatter_uses_the_real_media_type(png_path):
    formatted = format_claude_messages([{"image": png_path}])

    assert formatted[0]["content"][0]["source"]["media_type"] == "image/png"


def test_text_only_model_rejects_image_messages(png_path):
    """deepseek-v4-pro has no vision support; fail before building a request."""
    with pytest.raises(AssertionError, match="does not accept image input"):
        text_tools.prompt_llm(
            messages=[{"text": "what is this"}, {"image": png_path}],
            model="deepseek-v4-pro",
        )


def test_text_only_model_still_accepts_text_messages(monkeypatch):
    called = {}

    def fake_prompt_deepseek(**kwargs):
        called.update(kwargs)
        return {"text": "ok", "input_tokens": 1, "output_tokens": 1}

    monkeypatch.setattr(
        "aitools.third_party_apis.deepseek_tools.prompt_deepseek", fake_prompt_deepseek
    )

    result = text_tools.prompt_llm(messages=[{"text": "hi"}], model="deepseek-v4-pro")

    assert result == "ok"
    assert called["model"] == "deepseek-v4-pro"


def test_vision_model_accepts_image_messages(png_path, monkeypatch):
    def fake_prompt_deepseek(**kwargs):
        return {"text": "ok", "input_tokens": 1, "output_tokens": 1}

    monkeypatch.setattr(
        "aitools.third_party_apis.deepseek_tools.prompt_deepseek", fake_prompt_deepseek
    )

    assert text_tools.prompt_llm(
        messages=[{"image": png_path}], model="deepseek-flash"
    ) == "ok"
