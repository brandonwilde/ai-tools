#-------------Enable execution from non-root----------------#
import sys
from pathlib import Path
sys.path.append(str(next(p for p in Path(__file__).resolve().parents if p.name == 'ai-tools')))
#-----------------------------------------------------------#

from aitools.media_tools.text_tools import chat_with_llm


messages = [
    {"text": "When was the first time you heard about the concept of a chatbot?"}
]

def main(messages):
    chat_with_llm(messages, model="claude-3-haiku-20240307", cache=True)

if __name__ == "__main__":
    main(messages)