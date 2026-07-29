"""Image generation via the Gemini API ("Nano Banana").

Kept separate from `google_tools.py` because image generation uses the newer
`google-genai` SDK and the Interactions API, while the LLM helpers still use the
legacy `google-generativeai` package.

The response is wrapped so it matches the OpenAI/Recraft shape the rest of this
package expects: `response.data` is a list of objects carrying `b64_json`.
"""

import base64
import math
import mimetypes
import os
from dataclasses import dataclass, field
from pathlib import Path

from aitools.third_party_apis.models import (
    GOOGLE_IMAGE_GENERATORS,
    GoogleImageGenerators,
    GoogleImageSizes,
)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Aspect ratios the Gemini image models accept.
SUPPORTED_RATIOS = {
    "1:1": 1 / 1,
    "2:3": 2 / 3,
    "3:2": 3 / 2,
    "3:4": 3 / 4,
    "4:3": 4 / 3,
    "4:5": 4 / 5,
    "5:4": 5 / 4,
    "9:16": 9 / 16,
    "16:9": 16 / 9,
    "21:9": 21 / 9,
}


@dataclass
class _Image:
    b64_json: str
    url: None = None
    revised_prompt: None = None


@dataclass
class _Response:
    """Minimal stand-in for an OpenAI images response."""

    data: list = field(default_factory=list)


def size_to_aspect_ratio(size: str) -> str:
    """Convert a 'WxH' size string to the closest supported Gemini aspect ratio."""
    try:
        width, height = (int(n) for n in size.lower().split("x"))
    except ValueError:
        raise ValueError(f"Could not parse image size '{size}'. Expected e.g. '1024x1280'.")

    target = width / height
    return min(SUPPORTED_RATIOS, key=lambda r: abs(SUPPORTED_RATIOS[r] - target))


def _image_content(path) -> dict:
    """Build an Interactions API image content part from a file on disk."""
    path = Path(path)
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return {"type": "image", "data": data, "mime_type": mime_type}


def generate_image_via_google(
    prompt,
    model: GoogleImageGenerators = "gemini-3.1-flash-image",
    size: GoogleImageSizes = "1024x1024",
    style="",
    substyle="",
    num_variations=1,
    resolution=None,
    reference_images=None,
):
    """
    Generate an image using the Gemini API.

    `style`/`substyle` are accepted for signature compatibility with the other
    providers and folded into the prompt, since Gemini has no separate style
    parameter.

    `reference_images`, if given, is a list of image file paths passed to the
    model alongside the prompt (e.g. a real object that should appear
    consistently rather than be re-described from scratch each time).
    """
    if not GOOGLE_API_KEY:
        raise Exception("GOOGLE_API_KEY must be set as an environment variable.")

    try:
        from google import genai
    except ImportError:
        raise ImportError(
            "The google-genai package is required for Gemini image generation. "
            "Install it with `pip install google-genai`."
        )

    model_info = GOOGLE_IMAGE_GENERATORS[model]
    resolution = resolution or model_info["default_resolution"]
    assert resolution in model_info["resolutions"], (
        f"Resolution '{resolution}' is not valid for '{model}'. "
        f"Options: {model_info['resolutions']}."
    )

    if style:
        prompt = f"{prompt}\n\nStyle: {style}{f' / {substyle}' if substyle else ''}"

    if reference_images:
        model_input = [_image_content(p) for p in reference_images]
        model_input.append({"type": "text", "text": prompt})
    else:
        model_input = prompt

    client = genai.Client(api_key=GOOGLE_API_KEY)

    images = []
    # The Interactions API returns a single image per call, so variations are
    # separate requests.
    for _ in range(num_variations):
        interaction = client.interactions.create(
            model=model,
            input=model_input,
            response_format={
                "type": "image",
                "mime_type": "image/jpeg",
                "aspect_ratio": size_to_aspect_ratio(size),
                "image_size": resolution,
            },
        )
        images.append(_Image(b64_json=interaction.output_image.data))

    return _Response(data=images)
