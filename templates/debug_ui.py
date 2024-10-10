#-------------Enable execution from non-root----------------#
import sys
from pathlib import Path
sys.path.append(str(next(p for p in Path(__file__).resolve().parents if p.name == 'ai-tools')))
#-----------------------------------------------------------#

from aitools.media_tools.text_tools import prompt_llm


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