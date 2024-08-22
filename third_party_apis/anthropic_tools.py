import os
from typing import List

import anthropic

from third_party_apis.models import AnthropicLLMs
from media_tools.utils import encode_image

ANTHROPIC_API_KEY=os.environ.get('ANTHROPIC_API_KEY')
DEFAULT_ANTHROPIC_LLM = "claude-3-haiku-20240307"

# TODO: Update Anthropic prompt function to handle images as well.
# TODO: Add Anthropic chat function

if not ANTHROPIC_API_KEY:
    raise Exception("ANTHROPIC_API_KEY must be set as an environment variable.")

CLIENT = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)


def format_claude_messages(
    messages: List[dict] = [],
    system_prompt="",
):
    '''
    Format messages for submission to a Claude model.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
    - system_prompt (str): Not used here but included for consistency with OpenAI format function.
    '''

    user_content = []
    for message in messages:
        if 'text' in message:
            user_content.append({
                "type": "text",
                "text": message['text']
            })
        elif 'code' in message:
            user_content.append({
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
            user_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": f"image/{ext}",
                    "data": base64_image,
                }
            })

    formatted_messages = [{
        "role": "user",
        "content": user_content
    }]

    return formatted_messages


def prompt_claude(
    messages: List[dict],
    model:AnthropicLLMs = DEFAULT_ANTHROPIC_LLM,
    system_prompt="You are a helpful assistant.",
    max_tokens=1000,
    temperature=1,
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

    Returns:
    - str: The response from the LLM.
    """

    formatted_messages = format_claude_messages(messages)

    message = CLIENT.messages.create(
        model=model,
        system=system_prompt,
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
        system_prompt="You are a helpful assistant.",
        max_tokens=1024,
        temperature=1,
    ):
    """
    Stream a response from an Anthropic LLM.
    Prints the response as it is generated.
    """

    with CLIENT.messages.stream(
        model=model,
        system=system_prompt,
        messages=formatted_messages,
        max_tokens=max_tokens,
        temperature=temperature,
    ) as stream:
        full_response = ""
        for text_chunk in stream.text_stream:
            full_response += text_chunk
            print(text_chunk, end="", flush=True)

    return full_response