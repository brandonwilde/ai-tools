from aitools.media_tools.text_tools import prompt_llm


image_path = "data/IMG_20240210_115126.jpg"

messages = [
    {'text': "Please explain in detail what you see in this image."},
    {'image': image_path},
]

result = prompt_llm(messages, model="claude-3-haiku-20240307")

print(result)