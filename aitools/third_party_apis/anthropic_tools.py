import os
from typing import List, Literal, Union

import anthropic

from aitools.media_tools.utils import encode_image
from aitools.third_party_apis.models import ALL_LLMS, AnthropicLLMs

ANTHROPIC_API_KEY=os.environ.get('ANTHROPIC_API_KEY')
DEFAULT_ANTHROPIC_LLM = "claude-3-haiku-20240307"

DEFAULT_ANTHROPIC_LLM_INFO = ALL_LLMS[DEFAULT_ANTHROPIC_LLM]

if not ANTHROPIC_API_KEY:
    raise Exception("ANTHROPIC_API_KEY must be set as an environment variable.")

CLIENT = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)


def format_claude_messages(
    messages: List[Union[str,dict]] = [],
    role:Literal["system","user","assistant"] = "user",
    cache_messages=False,
):
    '''
    Format messages for submission to a Claude model.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
        If "cache" is also included in a message, a cache_control will be added after the message.
    - system_prompt (str): Not used here but included for consistency with OpenAI format function.
    - cache_messages (bool): Whether to cache the conversation. Will add cache_control after the last message.
    '''

    content = []
    for message in messages:
        if type(message) is str:
            message = {"text": message}
        if 'text' in message:
            content.append({
                "type": "text",
                "text": message['text']
            })
        elif 'code' in message:
            content.append({
                "type": "text",
                "text": f"```\n{message['code']}\n```"
            })
        elif 'image' in message:
            _, dot_ext = os.path.splitext(message['image'])
            ext = dot_ext.strip('.').lower()
            assert ext in ["png", "jpg", "jpeg", "gif", "webp"], f"Image must be a PNG, JPEG, GIF, or WEBP file, but you provided a {ext} file."
            if ext == "jpg":
                ext = "jpeg"
            base64_image = encode_image(message['image'])
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": f"image/{ext}",
                    "data": base64_image,
                }
            })
        if "cache" in message:
            content[-1]["cache_control"] = {"type": "ephemeral"}

    if cache_messages:
        content[-1]["cache_control"] = {"type": "ephemeral"}

    if role == "system":
        formatted_messages = content
    elif role == "user":
        formatted_messages = [{
            "role": "user",
            "content": content
        }]
    elif role == "assistant":
        formatted_messages = [{
            "role": "assistant",
            "content": content
        }]

    return formatted_messages


def prompt_claude(
    messages: List[Union[str,dict]],
    model:AnthropicLLMs = DEFAULT_ANTHROPIC_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
    max_tokens=DEFAULT_ANTHROPIC_LLM_INFO['output_limit'],
    temperature=1,
    json_mode=False,
):
    """
    Get a response from a Claude LLM.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
    - model (str): The Claude model to use.
    - system_prompt (str): The system prompt to use.
    - max_tokens (int): The maximum number of tokens to generate.
    - temperature (float): The temperature to use for token sampling.
    - json_mode (bool): Not used here but included for consistency with OpenAI prompt function.

    Returns:
    - str: The response from the LLM.
    """
    if isinstance(system_prompt, str):
        system_prompt = [system_prompt]
    formatted_system_prompt = format_claude_messages(system_prompt, role="system")
    formatted_messages = format_claude_messages(messages)

    message = CLIENT.messages.create(
        model=model,
        system=formatted_system_prompt,
        messages=formatted_messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return {
        "text": message.content[0].text,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
    }


def stream_claude(
    formatted_messages: List[dict],
    model:AnthropicLLMs = DEFAULT_ANTHROPIC_LLM,
    formatted_system_prompt:List[dict] = [{'text': "You are a helpful assistant."}],
    max_tokens=DEFAULT_ANTHROPIC_LLM_INFO['output_limit'],
    temperature=1,
    caching=False,
):
    """
    Stream a response from an Anthropic LLM.
    Prints the response as it is generated.
    """

    if caching:
        client_stream = CLIENT.beta.prompt_caching.messages.stream
    else:
        client_stream = CLIENT.messages.stream

    with client_stream(
        model=model,
        system=formatted_system_prompt,
        messages=formatted_messages,
        max_tokens=max_tokens,
        temperature=temperature,
    ) as stream:
        for text_chunk in stream.text_stream:
            print(text_chunk, end="", flush=True)

    response = {
        'text': stream.current_message_snapshot.content[0].text,
        'input_tokens': stream.current_message_snapshot.usage.input_tokens,
        'output_tokens': stream.current_message_snapshot.usage.output_tokens,
    }
    if caching:
        response['cache_write_tokens'] = stream.current_message_snapshot.usage.cache_creation_input_tokens
        response['cache_read_tokens'] = stream.current_message_snapshot.usage.cache_read_input_tokens

    return response