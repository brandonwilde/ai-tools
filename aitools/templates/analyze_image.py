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

from aitools.media_tools.text_tools import prompt_llm


image_path = "data/IMG_20240210_115126.jpg"

messages = [
    {'text': "Please explain in detail what you see in this image."},
    {'image': image_path},
]

result = prompt_llm(messages, model="claude-3-haiku-20240307")

print(result)