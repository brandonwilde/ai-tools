import json
from pathlib import Path
import requests
from tabulate import tabulate

from aitools.media_tools.image_tools import generate_image_via_openai
from aitools.media_tools.text_tools import prompt_llm
from aitools.media_tools.utils import increment_file_name


args = {
    "name": "9-25-blog",
    "blog_post": "", # Reads from file if empty
}

parent_dir = Path(__file__).parent

for arg in args:
    if not args[arg]:
        if (arg_path := parent_dir / f"{arg}.txt").exists():
            with open(arg_path, "r") as f:
                args[arg] = f.read()
        else:
            raise Exception(f"Please provide the {arg.replace('_',' ')} in the 'args' object at the top of the file or in a colocated file named '{arg}.txt'.")


prompt_template = """
I have a blog and I include an image with each blog post. Please help me generate an image for my latest blog post. The image should be relatively simple, as it will be a relatively small 128x128 header image for the blog post. Please provide 5 suggestions for the image based on the text of the blog post. Each suggestion should be a unique and creative description of the image that can be used to generate the image. Be creative, but please keep it simple and relevant to the blog post.

Response Format (JSON):
{{
    "images": [
        {{
            "description": "A description of the image.",
        }},
        ...
    ]
}}


Here is the blog post:

{BLOG_POST}
"""

prompt = prompt_template.format(
    BLOG_POST=args["blog_post"],
)

response = prompt_llm(
    messages=[{"text": prompt}],
    model="gpt-4o-mini",
    system_prompt="You are a helpful assistant.",
    max_tokens=1000,
    temperature=1,
    json_output=True,
)

def parse_response(response):
    parsed_response = json.loads(response)
    return parsed_response["images"]

print(response)

suggestions = parse_response(response)


# Print the suggestions in a table
data = []
for i, suggestion in enumerate(suggestions):
    data.append([f"Image {i+1}", suggestion["description"]])

print(tabulate(data, colalign=("left", "left")))

# Have user select which images to generate
selected_images = []
selected = input("Enter the numbers of the images you would like to generate, then hit Enter: ")
for i in selected:
    image_response = generate_image_via_openai(
        prompt=suggestions[int(i)-1]["description"],
        model='dall-e-3',
        size="1024x1024",
    )

    for image in image_response.data:
        if hasattr(image, 'revised_prompt'):
            print('Revised prompt:', image.revised_prompt)
        else:
            print('Original prompt used.')

        # download image
        image = requests.get(image.url)
        output_file_name = increment_file_name(args["name"] + f"-image-{int(i)}.png")

        with open(output_file_name, "wb") as file:
            file.write(image.content)

    