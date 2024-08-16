from typing import List

from media_tools.models import ALL_MODELS, ModelsList
from media_tools.utils import log_time

DEFAULT_LLM = "gpt-4o-mini"


@log_time
def prompt_llm(
    messages: List[dict],
    model:ModelsList = DEFAULT_LLM,
    system_prompt="You are a helpful assistant.",
    max_tokens=1000,
    temperature=1,
):
    """
    Get a response from an LLM.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
    - model (str): The LLM to use.
    - system_prompt (str): The system prompt to use.
    - max_tokens (int): The maximum number of tokens to generate.
    - temperature (float): The temperature to use for token sampling.

    Returns:
    - str: The response from the LLM.
    """
    
    model_info = ALL_MODELS[model]

    assert max_tokens <= model_info['output_limit'], f"Max_tokens must be less than or equal to {model_info['output_limit']} for {model}."

    provider = ALL_MODELS[model]['provider']

    if provider == "openai":
        from third_party_apis.openai_tools import prompt_openai as _prompt_model
    elif provider == "anthropic":
        from third_party_apis.anthropic_tools import prompt_claude as _prompt_model
    else:
        raise ValueError(f"Provider '{provider}' is not yet supported. Add basic prompting function for this provider.")

    response = _prompt_model(
        messages=messages,
        model=model,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )

    tok_in = response['input_tokens']
    tok_out = response['output_tokens']
    cost = tok_in * ALL_MODELS[model]['input_cost_per_M'] / 1000000 + \
        tok_out * ALL_MODELS[model]['output_cost_per_M'] / 1000000
    
    print(f"Prompt Tokens:   {tok_in:>7}")
    print(f"Response Tokens: {tok_out:>7}")
    print(f"Cost:           ${cost:.5f}")

    return response["text"]


def chat_with_llm(messages=[], model=DEFAULT_LLM, system_prompt="You are a helpful assistant."):
    """
    Conversational interface with the OpenAI API.
    Can optionally include a list of messages to start the conversation.
    """

    model_info = ALL_MODELS[model]
    if model_info['provider'] == "openai":
        from third_party_apis.openai_tools import chat_with_openai as _chat_with_llm
    else:
        raise ValueError(f"Provider '{model_info['provider']}' is not yet supported. Add chat function for this provider.")
    
    _chat_with_llm(
        messages=messages,
        model=model, 
        system_prompt=system_prompt
    )


def translate(text, target_lang="English", model:ModelsList = DEFAULT_LLM):
    """
    Translate text into a target language using the OpenAI API.
    """

    model_info = ALL_MODELS[model]
    messages = [
        {"text": f"Translate the following text into {target_lang.title()}."},
        {"text": text}
    ]
    system_prompt = "You are a highly skilled translator with expertise in many languages. Your task is to identify the language of the text I provide and accurately translate it into the specified target language while preserving the meaning, tone, and nuance of the original text. Please maintain proper grammar, spelling, and punctuation in the translated version. Do not provide any additional information or context beyond the translation itself."

    if model_info['provider'] == "openai":
        from third_party_apis.openai_tools import prompt_openai as _prompt_model
    elif model_info['provider'] == "anthropic":
        from third_party_apis.anthropic_tools import prompt_claude as _prompt_model
    else:
        raise ValueError(f"Provider '{model_info['provider']}' is not yet supported. Add basic prompting function for this provider.")
    
    translation = _prompt_model(
        messages=messages,
        model=model,
        system_prompt=system_prompt,
        temperature=1
    )

    return translation['text']