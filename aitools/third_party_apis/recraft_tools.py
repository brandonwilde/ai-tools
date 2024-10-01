import os
import requests

from openai import OpenAI

from aitools.third_party_apis.models import RecraftImageGenerators, RecraftImageSizes, RECRAFT_IMAGE_GENERATORS

RECRAFT_API_KEY=os.environ.get('RECRAFT_API_KEY')

if not RECRAFT_API_KEY:
    raise Exception("RECRAFT_API_KEY must be set as environment variable.")

CLIENT = OpenAI(
  base_url='https://external.api.recraft.ai/v1',
  api_key=RECRAFT_API_KEY,
)

url = "https://external.api.recraft.ai/v1/images/generations"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {RECRAFT_API_KEY}"
}

# Note: Style and substyle not currently working
def generate_image_via_recraft(
        prompt,
        model:RecraftImageGenerators ="recraft",
        size:RecraftImageSizes = "1024x1024",
        style ='',
        substyle='',
        num_variations=1,
        ):
    """
    Generate an image using the Recraft API.
    """

    model_info = RECRAFT_IMAGE_GENERATORS[model]
    assert size in model_info['sizes'], f"Size '{size}' is not valid for model '{model}'."


    # Define the payload
    payload = {
        "prompt": prompt,
        # "style": style,
        # "substyle": substyle,
        "size": size,
    }
    # response = requests.post(url, headers=headers, json=payload)


    response = CLIENT.images.generate(
        prompt=prompt,
        n=num_variations,
        size=size,
        # style=style,
        # extra_body={
        #     'substyle': substyle
        # }
    )

    return response