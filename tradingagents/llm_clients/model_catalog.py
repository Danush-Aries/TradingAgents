"""Shared model catalog for CLI selections and validation."""

from __future__ import annotations

from typing import Dict, List, Tuple

ModelOption = Tuple[str, str]
ProviderModeOptions = Dict[str, Dict[str, List[ModelOption]]]


MODEL_OPTIONS: ProviderModeOptions = {
    "openai": {
        "quick": [
            ("GPT-4.1 Mini - Fast, strong coding and tool use", "gpt-4.1-mini"),
            ("GPT-4.1 Nano - Cheapest, high-volume tasks", "gpt-4.1-nano"),
            ("GPT-4.1 - Flagship non-reasoning model", "gpt-4.1"),
            ("GPT-4o Mini - Cost-efficient, fast", "gpt-4o-mini"),
        ],
        "deep": [
            ("GPT-4.1 - Flagship non-reasoning model", "gpt-4.1"),
            ("GPT-4o - Multimodal, strong reasoning", "gpt-4o"),
            ("GPT-4.1 Mini - Fast, strong coding and tool use", "gpt-4.1-mini"),
            ("o4-Mini - Compact reasoning model", "o4-mini"),
        ],
    },
    "anthropic": {
        "quick": [
            ("Claude Sonnet 4.6 - Best speed and intelligence balance", "claude-sonnet-4-6"),
            ("Claude Haiku 4.5 - Fast, near-instant responses", "claude-haiku-4-5"),
            ("Claude Sonnet 4.5 - Agents and coding", "claude-sonnet-4-5"),
        ],
        "deep": [
            ("Claude Opus 4.5 - Premium, max intelligence", "claude-opus-4-5"),
            ("Claude Sonnet 4.6 - Best speed and intelligence balance", "claude-sonnet-4-6"),
            ("Claude Sonnet 4.5 - Agents and coding", "claude-sonnet-4-5"),
            ("Claude Haiku 4.5 - Fast, near-instant responses", "claude-haiku-4-5"),
        ],
    },
    "google": {
        "quick": [
            ("Gemini 2.5 Flash - Balanced, stable", "gemini-2.5-flash"),
            ("Gemini 2.5 Flash Lite - Fast, low-cost", "gemini-2.5-flash-lite"),
            ("Gemini 2.0 Flash - Fast, efficient", "gemini-2.0-flash"),
            ("Gemini 1.5 Flash - Proven, cost-effective", "gemini-1.5-flash"),
        ],
        "deep": [
            ("Gemini 2.5 Pro - Most capable Gemini model", "gemini-2.5-pro"),
            ("Gemini 2.5 Flash - Balanced, stable", "gemini-2.5-flash"),
            ("Gemini 1.5 Pro - Proven pro model", "gemini-1.5-pro"),
            ("Gemini 2.0 Flash - Fast, efficient", "gemini-2.0-flash"),
        ],
    },
    "xai": {
        "quick": [
            ("Grok 3 Fast - Speed optimized", "grok-3-fast"),
            ("Grok 3 Mini Fast - Efficient reasoning", "grok-3-mini-fast"),
            ("Grok Beta - Stable production model", "grok-beta"),
        ],
        "deep": [
            ("Grok 3 - Flagship model", "grok-3"),
            ("Grok 3 Fast - Speed optimized", "grok-3-fast"),
            ("Grok 3 Mini - Compact reasoning", "grok-3-mini"),
            ("Grok Beta - Stable production model", "grok-beta"),
        ],
    },
    "deepseek": {
        "quick": [
            ("DeepSeek Chat (V3) - Fast, efficient", "deepseek-chat"),
            ("Custom model ID", "custom"),
        ],
        "deep": [
            ("DeepSeek Reasoner (R1) - Extended thinking", "deepseek-reasoner"),
            ("DeepSeek Chat (V3) - Fast, efficient", "deepseek-chat"),
            ("Custom model ID", "custom"),
        ],
    },
    "qwen": {
        "quick": [
            ("Qwen Plus - Balanced model", "qwen-plus"),
            ("Qwen Turbo - Fast, cost-efficient", "qwen-turbo"),
            ("Custom model ID", "custom"),
        ],
        "deep": [
            ("Qwen Max - Most capable Qwen model", "qwen-max"),
            ("Qwen Plus - Balanced model", "qwen-plus"),
            ("Qwen Long - Long-context model", "qwen-long"),
            ("Custom model ID", "custom"),
        ],
    },
    "glm": {
        "quick": [
            ("GLM-4-Flash - Fast, cost-efficient", "glm-4-flash"),
            ("GLM-4-Air - Balanced speed/quality", "glm-4-air"),
            ("Custom model ID", "custom"),
        ],
        "deep": [
            ("GLM-4-Plus - High performance", "glm-4-plus"),
            ("GLM-4 - Standard model", "glm-4"),
            ("GLM-4-Air - Balanced speed/quality", "glm-4-air"),
            ("Custom model ID", "custom"),
        ],
    },
    # OpenRouter: fetched dynamically. Azure: any deployed model name.
    "ollama": {
        "quick": [
            ("Qwen3:latest (8B, local)", "qwen3:latest"),
            ("Llama3.2:latest (3B, local)", "llama3.2:latest"),
            ("Mistral:latest (7B, local)", "mistral:latest"),
        ],
        "deep": [
            ("Qwen3:32b (32B, local)", "qwen3:32b"),
            ("Llama3.3:latest (70B, local)", "llama3.3:latest"),
            ("Qwen3:latest (8B, local)", "qwen3:latest"),
        ],
    },
}


def get_model_options(provider: str, mode: str) -> List[ModelOption]:
    """Return shared model options for a provider and selection mode."""
    return MODEL_OPTIONS[provider.lower()][mode]


def get_known_models() -> Dict[str, List[str]]:
    """Build known model names from the shared CLI catalog."""
    return {
        provider: sorted(
            {
                value
                for options in mode_options.values()
                for _, value in options
            }
        )
        for provider, mode_options in MODEL_OPTIONS.items()
    }
