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


def ask_gpt4v(messages: list, max_tokens: int = 1000):
    '''
    Submit a prompt to the GPT-4 Vision model and return the response.

    Args:
    - messages (list): A list of messages to submit to the model. Each message is a dictionary with the following keys:
        - role (str): The role of the message, either "user" or "system".
        - content (list): A list of content items. Each content item is a dictionary with the following keys:
            - type (str): The type of content, either "text" or "image_url".
            - text (str): The text content.
            - image_url (dict): A dictionary with the following key:
                - path (str): The path to the image file.
    - max_tokens (int): The maximum number of tokens to generate.

    Returns:
    - response (str): The text response from the model.
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Organization": OPENAI_ORGANIZATION,
    }

    # Insert image content into the messages
    for message in messages:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'image_url':
                    image_path = content['image_url']['path']
                    base64_image = encode_image(image_path)
                    content['image_url']['url'] = f"data:image/jpeg;base64,{base64_image}"

    payload = {
        "model": "gpt-4-turbo",
        "messages": messages,
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']