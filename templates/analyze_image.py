#-------------Enable execution from non-root----------------#
import sys
from pathlib import Path
sys.path.append(str(next(p for p in Path(__file__).resolve().parents if p.name == 'ai-tools')))
#-----------------------------------------------------------#

from aitools.media_tools.text_tools import prompt_llm


image_path = "data/IMG_20240210_115126.jpg"

messages = [
    {'text': "Please explain in detail what you see in this image."},
    {'image': image_path},
]

result = prompt_llm(messages, model="claude-3-haiku-20240307")

print(result)