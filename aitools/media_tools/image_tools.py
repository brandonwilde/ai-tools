from typing import get_args, Literal

from aitools.third_party_apis.models import ImageGeneratorsList, ImageSizeList, ALL_IMAGE_GENERATORS

    
def generate_image(
        prompt,
        model:ImageGeneratorsList="dall-e-3",
        size:ImageSizeList = "1024x1024",
        style='',
        substyle='',
        num_variations=1,
        ):
    """
    Generate an image.
    """

    model_info = ALL_IMAGE_GENERATORS[model]

    if model_info['provider'] == "openai":
        from aitools.third_party_apis.openai_tools import generate_image_via_openai as _generate_image
    elif model_info['provider'] == "recraft":
        from aitools.third_party_apis.recraft_tools import generate_image_via_recraft as _generate_image

    response = _generate_image(
        model=model,
        prompt=prompt,
        size=size,
        style=style,
        substyle=substyle,
        num_variations=num_variations,
    )

    return response