import os
import requests

from openai import OpenAI


OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')

CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORGANIZATION,
)

output_file = "/home/brandon/Bilder/Generated/transcription_splash.png"

# add or increment the number in the output file name if it already exists
while os.path.exists(output_file):
    base, ext = os.path.splitext(output_file)
    if base[-1].isdigit():
        base = base[:-1] + str(int(base[-1]) + 1)
    else:
        base += "1"
    output_file = base + ext

# Create image
response = CLIENT.images.generate(
  model="dall-e-3",
  prompt="Percutaneous aortic valve implantation",
  n=1,
  size="1024x1792"
)

for image in response.data:
    print(image.revised_prompt)

    # download image
    image = requests.get(image.url)
    with open(output_file, "wb") as file:
        file.write(image.content)

    print()