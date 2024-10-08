import os
from typing import BinaryIO, List, Literal, Union

from openai import OpenAI

from aitools.media_tools.utils import encode_image
from aitools.third_party_apis.models import ALL_LLMS, OpenaiImageGenerators, OpenaiImageSizes, OpenaiLLMs, OpenaiSpeechRec, OPENAI_IMAGE_GENERATORS

OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')
DEFAULT_OPENAI_LLM = "gpt-4o-mini"
DEFAULT_OPENAI_SPEECH_REC = "whisper-1"

DEFAULT_OPENAI_LLM_INFO = ALL_LLMS[DEFAULT_OPENAI_LLM]

if any([not OPENAI_API_KEY, not OPENAI_ORGANIZATION]):
    raise Exception("OPENAI_API_KEY and OPENAI_ORGANIZATION must be set as environment variables.")

CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORGANIZATION,
)


def format_openai_messages(
    messages: List[Union[str,dict]] = [],
    role:Literal["system","user","assistant"] = "user",
    cache_messages=False,
):
    '''
    Format messages for submission to an OpenAI model.

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
            content.append({
                "type": "text",
                "text": message['text']
            })
        elif 'code' in message:
            content.append({
                "type": "text",
                "text": f"```html\n{message['code']}\n```"
            })
        elif 'image' in message:
            base64_image = encode_image(message['image'])
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
    
    if role == "system":
        formatted_messages = [{
            "role": "system",
            "content": content
        }]
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


def prompt_openai(
    messages: List[Union[str,dict]],
    model:OpenaiLLMs = DEFAULT_OPENAI_LLM,
    system_prompt:Union[str,List[Union[str,dict]]]="You are a helpful assistant.",
    max_tokens=DEFAULT_OPENAI_LLM_INFO['output_limit'],
    temperature=1,
    json_mode=False,
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
    - max_tokens (int): The maximum number of tokens to generate.
    - temperature (float): The temperature to use for token sampling.
    - json_mode (bool): Whether to return the response as a JSON object.

    Returns:
    - str: The response from the LLM.
    """

    formatted_system_prompt = format_openai_messages(system_prompt, role="system")
    formatted_messages = format_openai_messages(messages)
    system_and_messages = formatted_system_prompt + formatted_messages

    chat_response = CLIENT.chat.completions.create(
        model=model,
        messages=system_and_messages,
        max_tokens=max_tokens,
        temperature=temperature,
        response_format={
            "type": "json_object" if json_mode else "text",
        }
    )

    return {
        "text": chat_response.choices[0].message.content,
        "input_tokens": chat_response.usage.prompt_tokens - chat_response.usage.prompt_tokens_details.cached_tokens,
        "cache_read_tokens": chat_response.usage.prompt_tokens_details.cached_tokens,
        "output_tokens": chat_response.usage.completion_tokens,
    }


def stream_openai(
    formatted_messages: List[dict],
    model:OpenaiLLMs = DEFAULT_OPENAI_LLM,
    formatted_system_prompt:List[dict] = [{'text': "You are a helpful assistant."}],
    max_tokens=DEFAULT_OPENAI_LLM_INFO['output_limit'],
    temperature=1,
    caching=False,
):
    """
    Stream a response from an OpenAI LLM.
    Prints the response as it is generated.

    *Caching is done automatically, but param is included for consistency with Anthropic stream function.
    """

    chat_response = CLIENT.chat.completions.create(
        model=model,
        messages=formatted_system_prompt+formatted_messages,
        stream=True,
        stream_options={'include_usage': True},
        max_tokens=max_tokens,
        temperature=temperature,
    )

    collected_messages = []
    for chunk in chat_response:
        if chunk.choices:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message is not None:
                collected_messages.append(chunk_message)
                print(chunk.choices[0].delta.content, end='')

    response = {
        'text': ''.join(collected_messages),
        'input_tokens': chunk.usage.prompt_tokens,
        'output_tokens': chunk.usage.completion_tokens,
    }
    
    return response


def generate_image_via_openai(
        prompt,
        model:OpenaiImageGenerators ="dall-e-3",
        size:OpenaiImageSizes = "1024x1024",
        style='',
        substyle='',
        num_variations=1,
        ):
    """
    Generate an image using the OpenAI API.
    """

    model_info = OPENAI_IMAGE_GENERATORS[model]
    assert size in model_info['sizes'], f"Size '{size}' is not valid for model '{model}'."

    response = CLIENT.images.generate(
        model=model,
        prompt=prompt,
        n=num_variations,
        size=size
    )

    return response


def transcribe_via_openai(
    audio_file: BinaryIO,
    model:OpenaiSpeechRec = DEFAULT_OPENAI_SPEECH_REC,
):
    """
    Transcribe an audio file using an OpenAI speech recognition model.

    Args:
    - audio_file (BinaryIO): The MP3 audio file to transcribe.
    - model (str): The OpenAI speech recognition model to use.
    """

    transcription_response = CLIENT.audio.transcriptions.create(
        model=model, 
        file=audio_file,
        response_format='verbose_json',
    )

    return transcription_response