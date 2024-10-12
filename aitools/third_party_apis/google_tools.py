import os
from typing import List, Literal, Union

import google.generativeai as genai

from aitools.media_tools.utils import encode_image
from aitools.third_party_apis.models import ALL_LLMS, GoogleLLMs

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
DEFAULT_GOOGLE_LLM = "gemini-1.5-flash"

DEFAULT_GOOGLE_LLM_INFO = ALL_LLMS[DEFAULT_GOOGLE_LLM]


genai.configure(api_key=GOOGLE_API_KEY)



def format_gemini_messages(
    messages: List[Union[str,dict]] = [],
    role:Literal["system","user","assistant"] = "user",
    cache_messages=False,
) -> genai.types.ContentType:
    '''
    Format messages for submission to a Gemini model.

    Args:
    - messages (List[dict]): A list of messages to the LLM. Each message is a dictionary with one of the following fields:
        - text (str): A text message.
        - code (str): A code snippet.
        - image (str): The path to an image.
    - role (str): The role (system, user, assistant) of the message sender.
    - cache_messages (bool): Not used here but included for consistency with Anthropic format function.
    '''
    
    content = []
    for message in messages:
        if type(message) is str:
            message = {"text": message}
        if 'text' in message:
            content.append(message)
        elif 'code' in message:
            content.append({
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
                "inlineData": {
                    "mimeType": f"image/{ext}",
                    "data": base64_image,
                }
            })

    if role == "user":
        formatted_messages = [{
            "role": "user",
            "parts": content,
        }]
    elif role == "assistant":
        formatted_messages = [{
            "role": "model",
            "parts": content,
        }]
    elif role == "system":
        formatted_messages = {
            "parts": content,
        }

    return formatted_messages


def prompt_gemini(
    messages: List[Union[str,dict]],
    model:GoogleLLMs = DEFAULT_GOOGLE_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
    max_tokens=DEFAULT_GOOGLE_LLM_INFO['output_limit'],
    temperature=1,
    json_mode=False,
):
    
    formatted_messages = format_gemini_messages(messages)
    formatted_system_prompt = format_gemini_messages([system_prompt], role="system")
    
    CLIENT = genai.GenerativeModel(
        model_name=model,
        system_instruction=formatted_system_prompt,
    )

    response = CLIENT.generate_content(
        contents=formatted_messages,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
            response_mime_type='application/json' if json_mode else 'text/plain',
        )
    )

    return {
        "text": response.text,
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
    }