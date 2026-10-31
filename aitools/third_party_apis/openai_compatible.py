"""Shared request plumbing for providers that expose an OpenAI-compatible API."""
import os
from typing import Callable, List, Union

from openai import OpenAI

from aitools.third_party_apis.models import ALL_LLMS
from aitools.third_party_apis.openai_tools import format_openai_messages


def make_client_getter(api_key_env: str, base_url: str) -> Callable[[], OpenAI]:
    """
    Build a lazy, memoized accessor for one OpenAI-compatible endpoint.

    The key is read on first use rather than at import so that callers can set it
    after importing the module.
    """
    client = None

    def get_client() -> OpenAI:
        nonlocal client
        if client is None:
            api_key = os.environ.get(api_key_env)
            if not api_key:
                raise ValueError(f"{api_key_env} must be set as an environment variable.")
            client = OpenAI(api_key=api_key, base_url=base_url)
        return client

    return get_client


def extract_usage(usage) -> dict:
    """
    Map an OpenAI-compatible usage object onto this package's token fields.

    Providers report cache hits three different ways: DeepSeek splits the prompt into
    explicit hit/miss counts, OpenAI nests cached_tokens under prompt_tokens_details,
    and Moonshot reports cached_tokens at the top level. The latter two count cached
    tokens inside prompt_tokens, so they're subtracted back out to leave input_tokens
    holding only what bills at the full input rate.
    """
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    cache_hit = getattr(usage, "prompt_cache_hit_tokens", None)
    cache_miss = getattr(usage, "prompt_cache_miss_tokens", None)
    if cache_hit is not None and cache_miss is not None:
        return {
            "input_tokens": cache_miss,
            "cache_read_tokens": cache_hit,
            "output_tokens": completion_tokens,
        }

    cached = getattr(usage, "cached_tokens", None)
    if cached is None:
        details = getattr(usage, "prompt_tokens_details", None)
        cached = getattr(details, "cached_tokens", None) if details is not None else None

    if cached:
        # max() guards against a provider that reports the two counts exclusively.
        return {
            "input_tokens": max(prompt_tokens - cached, 0),
            "cache_read_tokens": cached,
            "output_tokens": completion_tokens,
        }

    return {
        "input_tokens": prompt_tokens,
        "output_tokens": completion_tokens,
    }


def prompt_openai_compatible(
    get_client: Callable[[], OpenAI],
    messages: List[Union[str, dict]],
    model: str,
    system_prompt: Union[str, List[Union[str, dict]]] = "You are a helpful assistant.",
    max_tokens=8192,
    temperature=None,
    json_mode=False,
    max_tokens_param="max_tokens",
):
    """
    Send a chat completion request to an OpenAI-compatible endpoint.

    Args:
    - get_client (callable): Returns the configured client for this provider.
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
    - model (str): The model to use.
    - system_prompt (str): The system prompt to use.
    - max_tokens (int): The maximum number of tokens to generate.
    - temperature (float): The temperature to use for token sampling. Omitted when None
        or when the model's catalog entry marks it unsupported.
    - json_mode (bool): Whether to return the response as a JSON object.
    - max_tokens_param (str): Name of the output-length parameter this endpoint expects.

    Returns:
    - dict: The response text and token usage.
    """

    formatted_system_prompt = format_openai_messages(system_prompt, role="system")
    formatted_messages = format_openai_messages(messages)
    system_and_messages = formatted_system_prompt + formatted_messages

    request_kwargs = {max_tokens_param: max_tokens}
    if temperature is not None and ALL_LLMS[model].get("supports_temperature", True):
        request_kwargs["temperature"] = temperature
    if json_mode:
        request_kwargs["response_format"] = {"type": "json_object"}

    chat_response = get_client().chat.completions.create(
        model=model,
        messages=system_and_messages,
        **request_kwargs,
    )

    return {
        "text": chat_response.choices[0].message.content,
        **extract_usage(chat_response.usage),
    }
