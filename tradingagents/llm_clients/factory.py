import os
import warnings
from typing import Optional

from .base_client import BaseLLMClient

# Providers that use the OpenAI-compatible chat completions API
_OPENAI_COMPATIBLE = (
    "openai", "xai", "deepseek", "qwen", "glm", "ollama", "openrouter",
)

# Map of provider -> environment variable that must be set
_PROVIDER_API_KEY_ENV = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "xai": "XAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
    "glm": "ZHIPU_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "azure": "AZURE_OPENAI_API_KEY",
    # ollama runs locally, no API key required
}


def _check_api_key(provider: str) -> None:
    """Emit an early warning when the required API key env var is not set.

    This surfaces the configuration problem at client construction time
    rather than at the first actual LLM call, making debugging easier.
    Ollama is excluded because it runs locally.
    """
    env_var = _PROVIDER_API_KEY_ENV.get(provider.lower())
    if env_var and not os.environ.get(env_var):
        warnings.warn(
            f"Environment variable '{env_var}' is not set. "
            f"Requests to '{provider}' will fail unless the key is provided "
            "another way (e.g. via the api_key kwarg).",
            RuntimeWarning,
            stacklevel=3,
        )


def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs,
) -> BaseLLMClient:
    """Create an LLM client for the specified provider.

    Provider modules are imported lazily so that simply importing this
    factory (e.g. during test collection) does not pull in heavy LLM SDKs
    or fail when their API keys are absent.

    Args:
        provider: LLM provider name (openai, anthropic, google, xai, deepseek,
                  qwen, glm, ollama, openrouter, azure)
        model: Model name/identifier
        base_url: Optional base URL for API endpoint
        **kwargs: Additional provider-specific arguments

    Returns:
        Configured BaseLLMClient instance

    Raises:
        ValueError: If provider is not supported
    """
    provider_lower = provider.lower()

    # Validate API key presence early so failures are obvious
    _check_api_key(provider_lower)

    if provider_lower in _OPENAI_COMPATIBLE:
        from .openai_client import OpenAIClient
        client = OpenAIClient(model, base_url, provider=provider_lower, **kwargs)
    elif provider_lower == "anthropic":
        from .anthropic_client import AnthropicClient
        client = AnthropicClient(model, base_url, **kwargs)
    elif provider_lower == "google":
        from .google_client import GoogleClient
        client = GoogleClient(model, base_url, **kwargs)
    elif provider_lower == "azure":
        from .azure_client import AzureOpenAIClient
        client = AzureOpenAIClient(model, base_url, **kwargs)
    else:
        raise ValueError(
            f"Unsupported LLM provider: '{provider}'. "
            f"Supported providers: openai, anthropic, google, xai, deepseek, "
            f"qwen, glm, ollama, openrouter, azure."
        )

    # Validate model name and emit a warning if it's unrecognised
    client.warn_if_unknown_model()
    return client
