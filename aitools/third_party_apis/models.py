from typing import Literal

# Keep this list updated for accurate type-checking
OpenaiLLMs = Literal[
    "gpt-4o",
    "gpt-4o-mini",
    "o1-mini",
    "gpt-3.5-turbo",
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
    "o1-mini": {
        "input_limit": 128000,
        "output_limit": 65536,
        "input_cost_per_M": 3.00,
        "cache_read_cost_per_M": 1.50,
        "output_cost_per_M": 12.00,
    },
    "gpt-3.5-turbo": {
        "input_limit": 16385,
        "output_limit": 4096,
        "input_cost_per_M": 0.50,
        "output_cost_per_M": 1.50,
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
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-haiku-20240307",
]
ANTHROPIC_LLM_INFO = {
    "max_temp": 1,
}
ANTHROPIC_LLMS = {
    "claude-3-5-sonnet-20241022": {
        "input_limit": 200000,
        "output_limit": 8192,
        "input_cost_per_M": 3,
        "cache_write_cost_per_M": 3.75,
        "cache_read_cost_per_M": 0.3,
        "output_cost_per_M": 15,
    },
    "claude-3-5-sonnet-20240620": {
        "input_limit": 200000,
        "output_limit": 8192,
        "input_cost_per_M": 3,
        "cache_write_cost_per_M": 3.75,
        "cache_read_cost_per_M": 0.3,
        "output_cost_per_M": 15,
    },
    "claude-3-haiku-20240307": {
        "input_limit": 200000,
        "output_limit": 4096,
        "input_cost_per_M": 0.25,
        "cache_write_cost_per_M": 0.3,
        "cache_read_cost_per_M": 0.03,
        "output_cost_per_M": 1.25,
    },
}

GoogleLLMs = Literal[
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
]
GOOGLE_LLM_INFO = {
    "max_temp": 2,
}
GOOGLE_LLMS = {
    "gemini-1.5-flash": {
        "input_limit": 1048576,
        "output_limit": 8192,
        "input_cost_per_M": 0.075, # up to 128k tokens, doubles after that
        "output_cost_per_M": 0.30, # up to 128k tokens, doubles after that
    },
    "gemini-1.5-flash-8b": {
        "input_limit": 1048576,
        "output_limit": 8192,
        "input_cost_per_M": 0.0375, # up to 128k tokens, doubles after that
        "output_cost_per_M": 0.15, # up to 128k tokens, doubles after that
    },
    "gemini-1.5-pro": {
        "input_limit": 2097152,
        "output_limit": 8192,
        "input_cost_per_M": 1.25, # up to 128k tokens, doubles after that
        "output_cost_per_M": 5, # up to 128k tokens, doubles after that
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

ALL_IMAGE_GENERATORS = {}
for model_name, model_data in OPENAI_IMAGE_GENERATORS.items():
    ALL_IMAGE_GENERATORS[model_name] = {**model_data, "provider": "openai"}
for model_name, model_data in RECRAFT_IMAGE_GENERATORS.items():
    ALL_IMAGE_GENERATORS[model_name] = {**model_data, "provider": "recraft"}

ALL_SPEECH_REC = {}
for model_name, model_data in OPENAI_SPEECH_REC.items():
    ALL_SPEECH_REC[model_name] = {**model_data, "provider": "openai"}

LLMsList = AnthropicLLMs | OpenaiLLMs | GoogleLLMs
ImageGeneratorsList = OpenaiImageGenerators | RecraftImageGenerators
ImageSizeList = OpenaiImageSizes | RecraftImageSizes
SpeechRecList = OpenaiSpeechRec