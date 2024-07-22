import os

import anthropic

ANTHROPIC_API_KEY=os.environ.get('ANTHROPIC_API_KEY')

if not ANTHROPIC_API_KEY:
    raise Exception("ANTHROPIC_API_KEY must be set as an environment variable.")

CLIENT = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)