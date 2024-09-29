from typing import List, Union

from tabulate import tabulate

from aitools.media_tools.utils import log_time
from aitools.third_party_apis.models import ALL_LLMS, LLMsList

DEFAULT_LLM = "gpt-4o-mini"


def log_token_usage(
    usage: dict,
    model:LLMsList = DEFAULT_LLM,
):
    '''
    Log the token usage and cost of a response from an LLM.
    '''

    tok_in = usage['input_tokens']
    tok_out = usage['output_tokens']
    tok_cache_write = usage['cache_write_tokens'] if 'cache_write_tokens' in usage else 0
    tok_cache_read = usage['cache_read_tokens'] if 'cache_read_tokens' in usage else 0

    cost = tok_in * ALL_LLMS[model]['input_cost_per_M'] / 1000000 \
        + tok_out * ALL_LLMS[model]['output_cost_per_M'] / 1000000 \
        + tok_cache_write * (ALL_LLMS[model]['cache_write_cost_per_M'] / 1000000  if tok_cache_write else 0) \
        + tok_cache_read * (ALL_LLMS[model]['cache_read_cost_per_M'] / 1000000 if tok_cache_read else 0)
    
    data = [
        ["Prompt Tokens", tok_in],
        ["Cache Write Tokens", tok_cache_write],
        ["Cache Read Tokens", tok_cache_read],
        ["Response Tokens", tok_out],
        ["Cost", f"${cost:.5f}"],
    ]

    print(tabulate(data, colalign=("left", "right")))

    return

@log_time
def prompt_llm(
    messages: List[Union[str,dict]],
    model:LLMsList = DEFAULT_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
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
    
    model_info = ALL_LLMS[model]

    assert max_tokens <= model_info['output_limit'], f"max_tokens must be less than or equal to {model_info['output_limit']} for {model}, but you requested up to {max_tokens} tokens."
    assert 0 <= temperature <= model_info['max_temp'], f"Permissible temperature values range from 0 to {model_info['max_temp']} for {model}, but you requested a temp of {temperature}."
    
    provider = ALL_LLMS[model]['provider']

    if provider == "openai":
        from aitools.third_party_apis.openai_tools import prompt_openai as _prompt_model
    elif provider == "anthropic":
        from aitools.third_party_apis.anthropic_tools import prompt_claude as _prompt_model
    else:
        raise ValueError(f"Provider '{provider}' is not yet supported. Add basic prompting function for this provider.")

    print(f'Calling LLM "{model}"...\n')

    response = _prompt_model(
        messages=messages,
        model=model,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )

    log_token_usage(response, model)

    return response["text"]


def chat_with_llm(
    messages:List[Union[str,dict]] = [],
    model:LLMsList = DEFAULT_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
    prefill_response="",
    max_tokens=1024,
    temperature=1,
    cache=True,
):
    """
    Conversational interface with an LLM.
    Can optionally include a list of messages to start the conversation.
    Specify prefill_response to provide the first words of the assistant's responses.
    Set cache to True to cache messages throughout the conversation. Generally a good idea for long conversations.
    """

    model_info = ALL_LLMS[model]
    if model_info['provider'] == "openai":
        from aitools.third_party_apis.openai_tools import (
            stream_openai as _stream_llm,
            format_openai_messages as _format_messages
        )
    elif model_info['provider'] == "anthropic":
        from aitools.third_party_apis.anthropic_tools import (
            stream_claude as _stream_llm,
            format_claude_messages as _format_messages
        )
    else:
        raise ValueError(f"Provider '{model_info['provider']}' is not yet supported. Add chat function for this provider.")
    
    if cache and model_info['provider'] != "anthropic":
        print(f"\n!!WARNING: Prompt caching is not yet supported for provider '{model_info['provider']}'. Disabling cache.\n")
        cache = False

    print(f'Calling LLM "{model}"...\n')

    if not messages:
        messages = [
            {
                "text": input("Start the conversation: ")
            }
        ]
        print()

    else:
        for m in messages:
            if 'text' in m:
                print("User:", m['text'], '\n')
            elif 'image' in m:
                print("User: [Image]", '\n')

    if isinstance(system_prompt, str):
        system_prompt = [system_prompt]
    formatted_system_prompt = _format_messages(system_prompt, role="system", cache_messages=cache)
    formatted_messages = _format_messages(messages, cache_messages=cache)
    
    usage = {}
    while True:
        try:
            print("Assistant: ", end='', flush=True)
            if prefill_response:
                formatted_messages.append({
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": prefill_response,
                        }
                    ]
                })

            response = _stream_llm(
                formatted_messages=formatted_messages,
                model=model,
                formatted_system_prompt=formatted_system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                caching=cache
            )
            print('\n')

            # Update usage
            for key in response:
                if 'token' in key:
                    usage[key] = usage.get(key, 0) + response[key]
                    
            if prefill_response:
                if cache and len(formatted_messages) >= 4:
                    # remove previous cache control - only use for the two most recent user messages
                    del formatted_messages[-4]['content'][-1]['cache_control']
                formatted_messages[-1]['content'][-1]['text'] += response['text']
            
            else:
                if cache and len(formatted_messages) >= 3:
                    # remove previous cache control - only use for the two most recent user messages
                    del formatted_messages[-3]['content'][-1]['cache_control']
                formatted_messages.append({
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": response['text']
                        }
                    ]
                })

            # Add user response
            message_content = {
                "type": "text",
                "text": input("User: "),
            }
            if cache:
                message_content["cache_control"] = {"type": "ephemeral"}

            formatted_messages.append({
                "role": "user",
                "content": [message_content]
            })

            print()

        except KeyboardInterrupt:
            print("\nEnding conversation.")
            break

    print()
    log_token_usage(usage, model)

    return


def translate(
    text: str,
    target_lang="English",
    model:LLMsList = DEFAULT_LLM
):
    """
    Translate text into a target language.
    """

    messages = [
        {"text": f"Translate the following text into {target_lang.title()}."},
        {"text": text}
    ]
    system_prompt = "You are a highly skilled translator with expertise in many languages. Your task is to identify the language of the text I provide and accurately translate it into the specified target language while preserving the meaning, tone, and nuance of the original text. Please maintain proper grammar, spelling, and punctuation in the translated version. Do not provide any additional information or context beyond the translation itself."

    translation = prompt_llm(
        messages=messages,
        model=model,
        system_prompt=system_prompt,
        temperature=0
    )

    return translation