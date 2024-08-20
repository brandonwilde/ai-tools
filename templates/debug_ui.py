from pathlib import Path
import sys

#----Enable imports as if run from project root----#
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
#--------------------------------------------------#

from media_tools.text_tools import prompt_llm


html_code = ""
js_code = ""
css_code = ""
system_prompt = "You are an expert software developer."
image_path = ""

messages = [
    {'text': """My code is not behaving as expected. Why is it that the job and education modals display the X (close button) and the modal content side by side (horizontally), but the business card modal displays the X and the modal content on top of each other (vertically)? I just added the book review modal and it is also displaying the X and the modal content on top of each other, but I would like it to display them side by side."""},
    # {'text': "Here is an image of the displayed webpage:"},
    # {'image': image_path},
    {'text': "Here is the `index.html` file:"},
    {'code': html_code},
    {'text': 'Here is the `main.js` file:'},
    {'code': js_code},
    {'text': "And here is `main.css` file:"},
    {'code': css_code},
    {'text': "How can I fix the alignment so that the book review modal content is to the right of the X rather than below it?"}
]

result = prompt_llm(messages, system_prompt=system_prompt)

print(result)