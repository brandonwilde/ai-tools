# ai-tools

A collection of general-purpose tools for processing text, documents, and images. Requires connecting to third-party APIs.

## Contents

New tools and providers are added as need arises. Currently included are the following tools and providers:

- LLM prompting - OpenAI, Anthropic, Google
- LLM chat - OpenAI, Anthropic
- Translation - OpenAI, Anthropic
- Image analysis - OpenAI, Anthropic
- Image generation - OpenAI, Recraft
- Audio transcription - OpenAI
- OCR - Azure

## Installation

After cloning the repository, install the required packages with
```bash
pip install -r requirements.txt
```

If you want to reduce the installation size, you can first remove any lines from `requirements.txt` corresponding to third-party providers you don't expect to use.

## Usage

The tools are generally intended to be called by other scripts. Example use cases are included in the `templates` directory. These can be executed directly or imported into other scripts.

## Usage in a separate project

To use the tools in a separate project, you can install this package from source with
```bash
pip install git+https://github.com/brandonwilde/ai-tools.git@main[<extras>]
```
Replace `<extras>` with a list of any extra dependencies you want to install. Options are `openai`, `anthropic`, `google`, `azure`, and `all`. Omitting `@main[<extras>]` to install only the base dependencies.

Then import the tools in your script with
```python
from ai_tools import <tool_name>
```