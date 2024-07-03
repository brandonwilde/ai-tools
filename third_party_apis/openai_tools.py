import os
from typing import List

from openai import OpenAI


OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')

if any([not OPENAI_API_KEY, not OPENAI_ORGANIZATION]):
    raise Exception("OPENAI_API_KEY and OPENAI_ORGANIZATION must be set as environment variables.")


CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORGANIZATION,
)


def format_openai_messages(messages: List[dict], system_prompt: str):
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
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "path": message['image']
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
