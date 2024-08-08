from typing import List

from media_tools.utils import encode_image, log_time

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"

# TODO: Update Anthropic LLM calls to handle images as well.


def format_openai_messages(messages: List[dict] = [], system_prompt=""):
    '''
    Format messages for submission to an OpenAI model.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
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
                "text": f"```html\n{message['code']}\n```"
            })
        elif 'image' in message:
            base64_image = encode_image(message['image'])
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
            
    formatted_system_prompt = [{
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": system_prompt,
            }
        ]
    }]

    if user_content:
        return formatted_system_prompt + [{
            "role": "user",
            "content": user_content
        }]

    return formatted_system_prompt


@log_time
def prompt_openai(
        messages: List[dict],
        model=DEFAULT_OPENAI_MODEL,
        system_prompt="You are a helpful assistant.",
    ):
    """
    Get a response from an OpenAI LLM.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
    - model (str): The OpenAI model to use.
    - system_prompt (str): The system prompt to use.

    Returns:
    - str: The response from the LLM.
    """

    from third_party_apis.openai_tools import (
        CLIENT as OPENAI_CLIENT,
    )

    formatted_messages = format_openai_messages(messages, system_prompt)

    chat_response = OPENAI_CLIENT.chat.completions.create(
        model=model,
        messages=formatted_messages,
    )

    print(f"Prompt Tokens:   {chat_response.usage.prompt_tokens:>7}")
    print(f"Response Tokens: {chat_response.usage.completion_tokens:>7}")

    return chat_response.choices[0].message.content


def chat_with_openai(messages=[], model=DEFAULT_OPENAI_MODEL, system_prompt="You are a helpful assistant."):
    """
    Conversational interface with the OpenAI API.
    Can optionally include a list of messages to start the conversation.
    """

    from third_party_apis.openai_tools import (
        CLIENT as OPENAI_CLIENT,
    )

    for m in messages:
        print("User:", m['text'], '\n')
        
    formatted_messages = format_openai_messages(messages, system_prompt)


    while True:
        chat_response = OPENAI_CLIENT.chat.completions.create(
            model=model,
            messages=formatted_messages,
            stream=True,
        )

        print("Assistant: ", end='')

        collected_messages = []
        for chunk in chat_response:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message is not None:
                collected_messages.append(chunk_message)
                print(chunk.choices[0].delta.content, end='')

        full_response = ''.join(collected_messages)
        print('\n')

        formatted_messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": full_response
                }
            ]
        })
        
        formatted_messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": input("User: ")
                }
            ]
        })
        print()


def translate_via_openai(text, target_lang="English", model=DEFAULT_OPENAI_MODEL):
    """
    Translate text into a target language using the OpenAI API.
    """

    translation = prompt_openai(
        messages=[
            {"text": f"Translate the following text into {target_lang.title()}."},
            {"text": text}
        ],
        model=model,
        system_prompt="You are a highly skilled translator with expertise in many languages. Your task is to identify the language of the text I provide and accurately translate it into the specified target language while preserving the meaning, tone, and nuance of the original text. Please maintain proper grammar, spelling, and punctuation in the translated version. Do not provide any additional information or context beyond the translation itself.",
    )

    return translation


@log_time
def prompt_claude(
        messages: List[dict],
        model=DEFAULT_ANTHROPIC_MODEL,
        system_prompt="You are a helpful assistant.",
        max_tokens=1000,
        temperature=0,
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

    from third_party_apis.anthropic_tools import (
        CLIENT as ANTHROPIC_CLIENT,
    )

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
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "path": message['image']
                }
            })

    formatted_messages = [{
        "role": "user",
        "content": user_content
    }]

    message = ANTHROPIC_CLIENT.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=formatted_messages
    )

    print(f"Prompt Tokens:   {message.usage.input_tokens:>7}")
    print(f"Response Tokens: {message.usage.output_tokens:>7}")

    return message.content[0].text


def translate_via_claude(text, target_lang="English", model=DEFAULT_ANTHROPIC_MODEL):
    """
    Translate text into a target language using the Anthropic API.
    """

    translation = prompt_claude(
        messages=[
            {"text": f"Translate the following text into {target_lang.title()}."},
            {"text": text}
        ],
        model=model,
        system_prompt="You are a highly skilled translator with expertise in many languages. Your task is to identify the language of the text I provide and accurately translate it into the specified target language while preserving the meaning, tone, and nuance of the original text. Please maintain proper grammar, spelling, and punctuation in the translated version. Do not provide any additional information or context beyond the translation itself.",
    )

    return translation