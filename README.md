# ai-tools

A collection of general-purpose tools for processing text, documents, and images. Requires connecting to third-party APIs.

## Installation

After cloning the repository, install the required packages with
```bash
pip install -r requirements.txt
```

If you want to reduce the installation size, you can first remove any lines from `requirements.txt` corresponding to third-party providers you don't expect to use.

## Usage

The tools are generally intended to be called by other scripts. Examples are included in the `templates` directory. To execute a template script, run
```bash
python -m templates.<template_name>
```