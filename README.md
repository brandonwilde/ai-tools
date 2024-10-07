# ai-tools

A collection of general-purpose tools for processing text, documents, and images. Requires connecting to third-party APIs.

## Contents

New tools and providers are added as need arises. Currently included are the following tools and providers:

- LLM prompting - OpenAI, Anthropic
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

The tools are generally intended to be called by other scripts. Example applications are included in the `templates` directory. To execute a template script, run
```bash
python -m templates.<template_name>
```