


def translate_via_openai(text, model="gpt-3.5-turbo"):
    """
    Translate text into English using the OpenAI API.
    """

    from openai_tools import CLIENT as OPENAI_CLIENT

    translation_response = OPENAI_CLIENT.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": "Translate the following text into English."}]},
                {"role": "user", "content": [{"type": "text", "text": text}]}
            ]
        )

    return translation_response.choices[0].message.content


