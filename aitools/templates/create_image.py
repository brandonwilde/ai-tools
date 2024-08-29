from pathlib import Path
import sys

#----Enable script execution as if run from project root----#
def find_repo_root(repo_name):
    current_path = Path(__file__).resolve()
    while current_path.parent != current_path: # Stop at filesystem root
        if current_path.name == repo_name:
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(f'Could not find the root of the "{repo_name}" repository in the file path.')

root_path = find_repo_root(repo_name="ai-tools")
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))
#-----------------------------------------------------------#

import requests

from aitools.media_tools.image_tools import generate_image_via_openai
from aitools.media_tools.utils import increment_file_name


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


output_file = "./rad_wildebeest.png"
prompt = "A rad wildebeest."
size = "512x512"
model = "dall-e-2"

create_image(prompt, output_file, model=model, size=size)