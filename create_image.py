import requests

from media_tools.image_tools import generate_image_via_openai
from utils import increment_file_name


def create_image(prompt, output_file, model="dall-e-3", size="1024x1024"):
    '''
    Create an image using the OpenAI API.
    '''

    # Create image
    image_response = generate_image_via_openai(prompt, model=model, size=size)

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


output_file = "./transcription_splash.png"
prompt = "A splash of color with the word 'transcription' in the center."
size = "512x512"
model = "dall-e-2"

create_image(prompt, output_file, model=model, size=size)