import base64
from typing import List, Literal

from third_party_apis.openai_tools import format_openai_messages


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

    from third_party_apis.openai_tools import CLIENT as OPENAI_CLIENT

    formatted_messages = format_openai_messages(messages, system_prompt)

    # Insert image content into the messages
    for message in formatted_messages:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'image_url':
                    image_path = content['image_url']['path']
                    base64_image = encode_image(image_path)
                    content['image_url']['url'] = f"data:image/jpeg;base64,{base64_image}"


    response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-4-turbo",
        messages=formatted_messages,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content