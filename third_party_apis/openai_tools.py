import os
from typing import List

from openai import OpenAI

from media_tools.utils import encode_image

OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

if any([not OPENAI_API_KEY, not OPENAI_ORGANIZATION]):
    raise Exception("OPENAI_API_KEY and OPENAI_ORGANIZATION must be set as environment variables.")

CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORGANIZATION,
)


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


def prompt_openai(
        messages: List[dict],
        model=DEFAULT_OPENAI_MODEL,
        system_prompt="You are a helpful assistant.",
        max_tokens=1000,
        temperature=1,
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

    formatted_messages = format_openai_messages(messages, system_prompt)

    chat_response = CLIENT.chat.completions.create(
        model=model,
        messages=formatted_messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return {
        "text": chat_response.choices[0].message.content,
        "input_tokens": chat_response.usage.prompt_tokens,
        "output_tokens": chat_response.usage.completion_tokens,
    }


def chat_with_openai(messages=[], model=DEFAULT_OPENAI_MODEL, system_prompt="You are a helpful assistant."):
    """
    Conversational interface with the OpenAI API.
    Can optionally include a list of messages to start the conversation.
    """

    for m in messages:
        print("User:", m['text'], '\n')
        
    formatted_messages = format_openai_messages(messages, system_prompt)


    while True:
        chat_response = CLIENT.chat.completions.create(
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