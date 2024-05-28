import base64
import json
import os

import requests

# OpenAI API Key
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')

# CLIENT = OpenAI(
#     api_key=OPENAI_API_KEY,
#     organization=OPENAI_ORGANIZATION,
# )

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def ask_gpt4v(image_path: str, messages: list, max_tokens: int = 1000):
    '''
    Submit a prompt to the GPT-4 Vision model and return the response. The prompt should be a list of messages, and there may be up to one image_url message in the list. The image_url message should have a URL field, which will be replaced with the base64-encoded image from the image_path argument.
    '''
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Organization": OPENAI_ORGANIZATION,
    }

    # Insert the image into the messages
    for message in messages:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'image_url':
                    content['image_url']['url'] = f"data:image/jpeg;base64,{base64_image}"

    payload = {
        "model": "gpt-4-turbo",
        "messages": messages,
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']