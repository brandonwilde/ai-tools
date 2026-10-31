# ai-tools [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/brandonwilde/ai-tools)

A collection of general-purpose tools for processing text, documents, and images. Requires connecting to third-party APIs.

## Contents

New tools and providers are added as need arises. Currently included are the following tools and providers:

- LLM prompting - OpenAI, Anthropic, Google, DeepSeek, Mistral, Moonshot
- LLM chat - OpenAI, Anthropic
- Translation - OpenAI, Anthropic
- Image analysis - OpenAI, Anthropic, Google, DeepSeek, Mistral, Moonshot
- Image generation - OpenAI, Recraft, Google
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

To use the tools in a separate project, install a tagged release from source with
```bash
pip install "aitools[<extras>] @ git+https://github.com/brandonwilde/ai-tools.git@vX.Y.Z"
```
Replace `<extras>` with a comma-separated list of extra dependencies. Options are `openai`, `anthropic`, `google`, `azure`, and `all`. Drop `[<extras>]` to install only the base dependencies.

Replace `vX.Y.Z` with a version from [Releases](https://github.com/brandonwilde/ai-tools/releases), or with `main` to get unreleased changes.

Then import the tools in your script with
```python
from aitools.media_tools.text_tools import prompt_llm
```
