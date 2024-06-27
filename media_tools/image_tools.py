import base64
import os
from typing import List, Literal

import requests

# TODO: Update multimodal model request to use Python API 


def generate_image_via_openai(
        prompt,
        model="dall-e-3",
        size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1792",
        # quality,
        # style,
        ):
    """
    Generate an image using the OpenAI API.
    """

    from third_party_apis.openai_tools import CLIENT

    response = CLIENT.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size=size
    )

    return response


# OpenAI API Key
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')


def format_messages(messages: List[dict], system_prompt: str):
    '''
    Debug a user interface using the GPT-4 Vision model.

    Args:
    - messages (List[dict]): A list of messages to the multimodal LLM. Each message is a dictionary with one of the following keys:
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
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "path": message['image']
                }
            })
    
    messages_with_system_prompt = [{
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": system_prompt,
            }
        ]
    },
    {
        "role": "user",
        "content": user_content
    }]

    return messages_with_system_prompt


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def ask_gpt4v(messages: List[dict], system_prompt: str, max_tokens: int = 1000):
    '''
    Submit a prompt to the GPT-4 Vision model and return the response.

    Args:
    - messages (List[dict]): A list of messages to the multimodal LLM. Each message is a dictionary with one of the following keys:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
    - system_prompt (str): The system prompt to provide context to the model.
    - max_tokens (int): The maximum number of tokens to generate.

    Returns:
    - response (str): The text response from the model.
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Organization": OPENAI_ORGANIZATION,
    }

    formatted_messages = format_messages(messages, system_prompt)

    # Insert image content into the messages
    for message in formatted_messages:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'image_url':
                    image_path = content['image_url']['path']
                    base64_image = encode_image(image_path)
                    content['image_url']['url'] = f"data:image/jpeg;base64,{base64_image}"

    payload = {
        "model": "gpt-4-turbo",
        "messages": formatted_messages,
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']