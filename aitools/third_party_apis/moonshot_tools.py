from typing import List, Union

from aitools.third_party_apis.models import ALL_LLMS, MoonshotLLMs
from aitools.third_party_apis.openai_compatible import make_client_getter, prompt_openai_compatible

MOONSHOT_BASE_URL = "https://api.moonshot.ai/v1"
DEFAULT_MOONSHOT_LLM = "kimi-k3"

DEFAULT_MOONSHOT_LLM_INFO = ALL_LLMS[DEFAULT_MOONSHOT_LLM]

_get_client = make_client_getter("MOONSHOT_API_KEY", MOONSHOT_BASE_URL)


def prompt_kimi(
    messages: List[Union[str,dict]],
    model:MoonshotLLMs = DEFAULT_MOONSHOT_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
    max_tokens=8192,
    temperature=None,
    json_mode=False,
):
    """
    Get a response from a Kimi (Moonshot AI) LLM (OpenAI-compatible API).

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
    - model (str): The Kimi model to use.
    - system_prompt (str): The system prompt to use.
    - max_tokens (int): The maximum number of tokens to generate.
    - temperature (float): Accepted for signature parity but never sent; every Kimi model
        fixes its sampling parameters and errors on an explicit value.
    - json_mode (bool): Whether to return the response as a JSON object.

    Returns:
    - dict: The response text and token usage.
    """

    return prompt_openai_compatible(
        get_client=_get_client,
        messages=messages,
        model=model,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        json_mode=json_mode,
        max_tokens_param="max_completion_tokens",
    )
