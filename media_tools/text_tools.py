from typing import List

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

def prompt_openai(messages: List[dict], model=DEFAULT_OPENAI_MODEL, system_prompt="You are a helpful assistant."):
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
        format_openai_messages,
    )

    formatted_messages = format_openai_messages(messages, system_prompt)

    chat_response = OPENAI_CLIENT.chat.completions.create(
        model=model,
        messages=formatted_messages,
    )

    return chat_response.choices[0].message.content


def chat_with_openai(messages=[], model=DEFAULT_OPENAI_MODEL, system_prompt="You are a helpful assistant."):
    """
    Conversational interface with the OpenAI API.
    Can optionally include a list of messages to start the conversation.
    """

    from third_party_apis.openai_tools import (
        CLIENT as OPENAI_CLIENT,
        format_openai_messages,
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



def translate_via_openai(text, model=DEFAULT_OPENAI_MODEL):
    """
    Translate text into English using the OpenAI API.
    """

    from third_party_apis.openai_tools import CLIENT as OPENAI_CLIENT

    translation_response = OPENAI_CLIENT.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": "Translate the following text into English."}]},
                {"role": "user", "content": [{"type": "text", "text": text}]}
            ]
        )

    return translation_response.choices[0].message.content


