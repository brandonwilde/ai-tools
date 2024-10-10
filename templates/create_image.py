#-------------Enable execution from non-root----------------#
import sys
from pathlib import Path
sys.path.append(str(next(p for p in Path(__file__).resolve().parents if p.name == 'ai-tools')))
#-----------------------------------------------------------#

import requests

from aitools.media_tools.image_tools import generate_image
from aitools.media_tools.utils import increment_file_name


def create_image(
        prompt,
        output_file,
        model="dall-e-3",
        size="1024x1024",
        style='',
        substyle='',
    ):
    '''
    Create an image using the OpenAI API.
    '''

    # Create image
    image_response = generate_image(prompt, model=model, size=size)

    for image in image_response.data:
        if hasattr(image, 'revised_prompt'):
            print('Revised prompt:', image.revised_prompt)
        else:
            print('Original prompt used.')

        # download image
        image = requests.get(image.url)
        output_file_name = increment_file_name(output_file)

        with open(output_file_name, "wb") as file:
            file.write(image.content)

    return


output_file = "./clock2.png"
prompt = "A simple clock."
size = "1024x1024"
model = "recraft"

create_image(prompt, output_file, model=model, size=size)