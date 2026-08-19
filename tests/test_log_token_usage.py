"""Pin the cost-calculation math in log_token_usage against a known model."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aitools.media_tools.text_tools import log_token_usage  # noqa: E402


def test_log_token_usage_cost_with_cache_tokens(capsys):
    # Model with recorded cache prices.
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_write_tokens": 2000,
        "cache_read_tokens": 3000,
    }

    log_token_usage(usage, model="claude-haiku-4-5")

    captured = capsys.readouterr().out
    assert "$0.00630" in captured


def test_log_token_usage_cost_without_cache_tokens(capsys):
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
    }

    log_token_usage(usage, model="claude-haiku-4-5")

    captured = capsys.readouterr().out
    assert "$0.00350" in captured


def test_log_token_usage_falls_back_to_input_rate_for_missing_cache_read_price(capsys):
    # Model without recorded cache prices must not raise; estimate at input rate.
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_read_tokens": 2000,
    }

    log_token_usage(usage, model="gemini-3.5-flash")

    captured = capsys.readouterr().out
    assert "$0.00900" in captured
    assert "est. @ input rate" in captured


def test_log_token_usage_falls_back_to_input_rate_for_missing_cache_write_price(capsys):
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_write_tokens": 2000,
    }

    log_token_usage(usage, model="gemini-3.5-flash")

    captured = capsys.readouterr().out
    assert "$0.00900" in captured
    assert "est. @ input rate" in captured


def test_log_token_usage_uses_real_cache_price_when_available(capsys):
    # Ensure models with recorded cache prices do not use the fallback.
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_write_tokens": 2000,
        "cache_read_tokens": 3000,
    }

    log_token_usage(usage, model="claude-haiku-4-5")

    captured = capsys.readouterr().out
    assert "$0.00630" in captured
    assert "est. @ input rate" not in captured
