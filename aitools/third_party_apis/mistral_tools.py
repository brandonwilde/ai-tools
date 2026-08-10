import os
from typing import List, Union

from openai import OpenAI

from aitools.third_party_apis.models import ALL_LLMS, MistralLLMs
from aitools.third_party_apis.openai_tools import format_openai_messages

MISTRAL_API_KEY=os.environ.get('MISTRAL_API_KEY')
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
DEFAULT_MISTRAL_LLM = "mistral-medium-latest"

DEFAULT_MISTRAL_LLM_INFO = ALL_LLMS[DEFAULT_MISTRAL_LLM]

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY must be set as an environment variable.")
        _client = OpenAI(api_key=MISTRAL_API_KEY, base_url=MISTRAL_BASE_URL)
    return _client


def prompt_mistral(
    messages: List[Union[str,dict]],
    model:MistralLLMs = DEFAULT_MISTRAL_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
    max_tokens=8192,
    temperature=None,
    json_mode=False,
):
    """
    Get a response from a Mistral LLM (OpenAI-compatible API).

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
    - model (str): The Mistral model to use.
    - system_prompt (str): The system prompt to use.
    - max_tokens (int): The maximum number of tokens to generate.
    - temperature (float): The temperature to use for token sampling. Omitted when None.
    - json_mode (bool): Whether to return the response as a JSON object.

    Returns:
    - dict: The response text and token usage.
    """

    formatted_system_prompt = format_openai_messages(system_prompt, role="system")
    formatted_messages = format_openai_messages(messages)
    system_and_messages = formatted_system_prompt + formatted_messages

    request_kwargs = {}
    if temperature is not None:
        request_kwargs["temperature"] = temperature
    if json_mode:
        request_kwargs["response_format"] = {"type": "json_object"}

    chat_response = _get_client().chat.completions.create(
        model=model,
        messages=system_and_messages,
        max_tokens=max_tokens,
        **request_kwargs,
    )

    return {
        "text": chat_response.choices[0].message.content,
        "input_tokens": chat_response.usage.prompt_tokens,
        "output_tokens": chat_response.usage.completion_tokens,
    }
