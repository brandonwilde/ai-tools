from aitools.media_tools.text_tools import chat_with_llm


messages = [
    {"text": "When was the first time you heard about the concept of a chatbot?"}
]

chat_with_llm(messages, model="claude-3-haiku-20240307", cache=True)