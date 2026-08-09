"""Pin the cost-calculation math in log_token_usage against a known model."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aitools.media_tools.text_tools import log_token_usage  # noqa: E402


def test_log_token_usage_cost_with_cache_tokens(capsys):
    # claude-haiku-4-5: input 1.00/M, output 5.00/M, cache_write 1.25/M, cache_read 0.10/M
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_write_tokens": 2000,
        "cache_read_tokens": 3000,
    }

    log_token_usage(usage, model="claude-haiku-4-5")

    captured = capsys.readouterr().out
    # 1000*1.00/1e6 + 500*5.00/1e6 + 2000*1.25/1e6 + 3000*0.10/1e6 = 0.0063
    assert "$0.00630" in captured


def test_log_token_usage_cost_without_cache_tokens(capsys):
    usage = {
        "input_tokens": 1000,
        "output_tokens": 500,
    }

    log_token_usage(usage, model="claude-haiku-4-5")

    captured = capsys.readouterr().out
    # 1000*1.00/1e6 + 500*5.00/1e6 = 0.0035; no cache tokens billed
    assert "$0.00350" in captured
