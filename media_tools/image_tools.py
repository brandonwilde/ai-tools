from typing import List, Literal


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

    from third_party_apis.openai_tools import CLIENT as OPENAI_CLIENT

    response = OPENAI_CLIENT.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size=size
    )

    return response