from typing import Literal

# Keep this list updated for accurate type-checking
OpenaiLLMs = Literal[
    "gpt-5.5",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-4o",
    "gpt-4o-mini",
]
OpenaiImageGenerators = Literal[
    "dall-e-2",
    "dall-e-3",
]
OpenaiSpeechRec = Literal[
    "whisper-1",
]
OpenaiImageSizes = Literal[
    "256x256",
    "512x512",
    "1024x1024",
    "1792x1024",
    "1024x1792",
]

OPENAI_LLM_INFO = {
    "max_temp": 2,
}
OPENAI_LLMS = {
    # GPT-5.x models reject the temperature parameter and require
    # max_completion_tokens instead of max_tokens.
    "gpt-5.5": {
        "input_limit": 400000,
        "output_limit": 128000,
        "input_cost_per_M": 5.00,  # long-context (>272k input) doubles to 10.00
        "cache_read_cost_per_M": 0.50,
        "output_cost_per_M": 30.00,
        "supports_temperature": False,
    },
    "gpt-5.4": {
        "input_limit": 400000,
        "output_limit": 128000,
        "input_cost_per_M": 2.50,
        "cache_read_cost_per_M": 0.25,
        "output_cost_per_M": 15.00,
        "supports_temperature": False,
    },
    "gpt-5.4-mini": {
        "input_limit": 400000,
        "output_limit": 128000,
        "input_cost_per_M": 0.75,
        "cache_read_cost_per_M": 0.075,
        "output_cost_per_M": 4.50,
        "supports_temperature": False,
    },
    "gpt-4o": {
        "input_limit": 128000,
        "output_limit": 16384,
        "input_cost_per_M": 2.50,
        "cache_read_cost_per_M": 1.25,
        "output_cost_per_M": 10,
    },
    "gpt-4o-mini": {
        "input_limit": 128000,
        "output_limit": 16384,
        "input_cost_per_M": 0.15,
        "cache_read_cost_per_M": 0.075,
        "output_cost_per_M": 0.60,
    },
}
OPENAI_IMAGE_GENERATORS = {
    "dall-e-2": {
        "sizes": ["256x256", "512x512", "1024x1024"],
    },
    "dall-e-3": {
        "sizes": ["1024x1024", "1792x1024", "1024x1792"],
    },
}
OPENAI_SPEECH_REC = {
    "whisper-1": {
        "cost_per_min": 0.0006,
    },
}


AnthropicLLMs = Literal[
    "claude-opus-4-8",
    "claude-sonnet-5",
    "claude-haiku-4-5",
]
ANTHROPIC_LLM_INFO = {
    "max_temp": 1,
}
ANTHROPIC_LLMS = {
    # Opus 4.8 and Sonnet 5 reject non-default temperature/top_p/top_k.
    "claude-opus-4-8": {
        "input_limit": 1000000,
        "output_limit": 128000,  # requires streaming above ~16k
        "input_cost_per_M": 5.00,
        "cache_write_cost_per_M": 6.25,
        "cache_read_cost_per_M": 0.50,
        "output_cost_per_M": 25.00,
        "supports_temperature": False,
    },
    "claude-sonnet-5": {
        "input_limit": 1000000,
        "output_limit": 128000,
        "input_cost_per_M": 3.00,  # intro pricing 2.00 through 2026-08-31
        "cache_write_cost_per_M": 3.75,
        "cache_read_cost_per_M": 0.30,
        "output_cost_per_M": 15.00,  # intro pricing 10.00 through 2026-08-31
        "supports_temperature": False,
    },
    "claude-haiku-4-5": {
        "input_limit": 200000,
        "output_limit": 64000,
        "input_cost_per_M": 1.00,
        "cache_write_cost_per_M": 1.25,
        "cache_read_cost_per_M": 0.10,
        "output_cost_per_M": 5.00,
    },
}

GoogleLLMs = Literal[
    "gemini-3.1-pro-preview",
    "gemini-3.5-flash",
]
GOOGLE_LLM_INFO = {
    "max_temp": 2,
}
GOOGLE_LLMS = {
    "gemini-3.1-pro-preview": {
        "input_limit": 1048576,
        "output_limit": 65536,
        "input_cost_per_M": 2.00,  # up to 200k tokens, 4.00 after that
        "output_cost_per_M": 12.00,  # up to 200k tokens, 18.00 after that
    },
    "gemini-3.5-flash": {
        "input_limit": 1048576,
        "output_limit": 65536,
        "input_cost_per_M": 1.50,
        "output_cost_per_M": 9.00,
    },
}

DeepseekLLMs = Literal[
    "deepseek-v4-pro",
    "deepseek-v4-flash",
]
DEEPSEEK_LLM_INFO = {
    "max_temp": 2,
}
DEEPSEEK_LLMS = {
    # deepseek-chat / deepseek-reasoner names are deprecated as of 2026-07-24
    "deepseek-v4-pro": {
        "input_limit": 1000000,
        "output_limit": 384000,
        "input_cost_per_M": 0.435,
        "cache_read_cost_per_M": 0.003625,
        "output_cost_per_M": 0.87,
    },
    "deepseek-v4-flash": {
        "input_limit": 1000000,
        "output_limit": 384000,
        "input_cost_per_M": 0.14,
        "cache_read_cost_per_M": 0.0028,
        "output_cost_per_M": 0.28,
    },
}

MistralLLMs = Literal[
    "mistral-large-latest",
    "mistral-medium-latest",
]
MISTRAL_LLM_INFO = {
    "max_temp": 1,
}
MISTRAL_LLMS = {
    "mistral-large-latest": {  # currently Mistral Large 3
        "input_limit": 256000,
        "output_limit": 32000,
        "input_cost_per_M": 0.50,
        "output_cost_per_M": 1.50,
    },
    "mistral-medium-latest": {  # currently Mistral Medium 3
        "input_limit": 128000,
        "output_limit": 32000,
        "input_cost_per_M": 0.40,
        "output_cost_per_M": 2.00,
    },
}

RecraftImageGenerators = Literal[
    "recraft",
]
RecraftImageSizes = Literal[
    "1024x1024",
    "1365x1024",
    "1024x1365",
    "1536x1024",
    "1024x1536",
    "1820x1024",
    "1024x1820",
    "1024x2048",
    "2048x1024",
    "1434x1024",
    "1024x1434",
    "1024x1280",
    "1280x1024",
    "1024x1707",
    "1707x1024",
]
RECRAFT_IMAGE_GENERATORS = {
    "recraft": {
        "sizes": [ "1024x1024", "1365x1024", "1024x1365", "1536x1024", "1024x1536", "1820x1024", "1024x1820", "1024x2048", "2048x1024", "1434x1024", "1024x1434", "1024x1280", "1280x1024", "1024x1707", "1707x1024"],
    },
}

ALL_LLMS = {}
for model_name, model_data in OPENAI_LLMS.items():
    ALL_LLMS[model_name] = {**model_data, "provider": "openai", **OPENAI_LLM_INFO}
for model_name, model_data in ANTHROPIC_LLMS.items():
    ALL_LLMS[model_name] = {**model_data, "provider": "anthropic", **ANTHROPIC_LLM_INFO}
for model_name, model_data in GOOGLE_LLMS.items():
    ALL_LLMS[model_name] = {**model_data, "provider": "google", **GOOGLE_LLM_INFO}
for model_name, model_data in DEEPSEEK_LLMS.items():
    ALL_LLMS[model_name] = {**model_data, "provider": "deepseek", **DEEPSEEK_LLM_INFO}
for model_name, model_data in MISTRAL_LLMS.items():
    ALL_LLMS[model_name] = {**model_data, "provider": "mistral", **MISTRAL_LLM_INFO}

ALL_IMAGE_GENERATORS = {}
for model_name, model_data in OPENAI_IMAGE_GENERATORS.items():
    ALL_IMAGE_GENERATORS[model_name] = {**model_data, "provider": "openai"}
for model_name, model_data in RECRAFT_IMAGE_GENERATORS.items():
    ALL_IMAGE_GENERATORS[model_name] = {**model_data, "provider": "recraft"}

ALL_SPEECH_REC = {}
for model_name, model_data in OPENAI_SPEECH_REC.items():
    ALL_SPEECH_REC[model_name] = {**model_data, "provider": "openai"}

LLMsList = AnthropicLLMs | OpenaiLLMs | GoogleLLMs | DeepseekLLMs | MistralLLMs
ImageGeneratorsList = OpenaiImageGenerators | RecraftImageGenerators
ImageSizeList = OpenaiImageSizes | RecraftImageSizes
SpeechRecList = OpenaiSpeechRec
