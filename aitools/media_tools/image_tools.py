from typing import get_args, Literal

from aitools.third_party_apis.models import ImageGeneratorsList, ImageSizeList, ALL_IMAGE_GENERATORS

    
def generate_image(
        prompt,
        model:ImageGeneratorsList="dall-e-3",
        size:ImageSizeList = "1024x1024",
        style='',
        substyle='',
        num_variations=1,
        reference_images=None,
        ):
    """
    Generate an image.

    `reference_images`, if given, is a list of image file paths to pass to the
    model alongside the prompt. Only supported by models with
    `supports_reference_images` set in their registry entry (currently the
    Gemini and gpt-image-1 models) — other models will raise if given
    reference images.
    """

    model_info = ALL_IMAGE_GENERATORS[model]

    if model_info['provider'] == "openai":
        from aitools.third_party_apis.openai_tools import generate_image_via_openai as _generate_image
    elif model_info['provider'] == "recraft":
        from aitools.third_party_apis.recraft_tools import generate_image_via_recraft as _generate_image
    elif model_info['provider'] == "google":
        from aitools.third_party_apis.google_image_tools import generate_image_via_google as _generate_image

    kwargs = {}
    if reference_images:
        if not model_info.get('supports_reference_images'):
            raise ValueError(
                f"reference_images isn't supported for model '{model}'. "
                f"Use a model with supports_reference_images set instead."
            )
        kwargs['reference_images'] = reference_images

    response = _generate_image(
        model=model,
        prompt=prompt,
        size=size,
        style=style,
        substyle=substyle,
        num_variations=num_variations,
        **kwargs,
    )

    return response