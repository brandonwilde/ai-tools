from typing import Literal

# Keep this list updated for accurate type-checking
ModelsList = Literal[
    "gpt-4o-mini",
    "gpt-3.5-turbo",
    "claude-3-5-sonnet-20240620",
    "claude-3-haiku-20240307",
    ]

ALL_MODELS = {}

OPENAI_MODELS = {
    "gpt-4o-mini": {
        "input_limit": 128000,
        "output_limit": 16384,
        "input_cost_per_M": 0.15,
        "output_cost_per_M": 0.60,
    },
    "gpt-3.5-turbo": {
        "input_limit": 16385,
        "output_limit": 4096,
        "input_cost_per_M": 0.50,
        "output_cost_per_M": 1.50,
    },
}
for model_name, model_data in OPENAI_MODELS.items():
    ALL_MODELS[model_name] = {**model_data, "provider": "openai"}


ANTHROPIC_MODELS = {
    "claude-3-5-sonnet-20240620": {
        "input_limit": 200000,
        "output_limit": 8192,
        "input_cost_per_M": 3,
        "output_cost_per_M": 15,
    },
    "claude-3-haiku-20240307": {
        "input_limit": 200000,
        "output_limit": 4096,
        "input_cost_per_M": 0.25,
        "output_cost_per_M": 1.25,
    },
}
for model_name, model_data in ANTHROPIC_MODELS.items():
    ALL_MODELS[model_name] = {**model_data, "provider": "anthropic"}