from functools import lru_cache
from openai import OpenAI
from pydantic import BaseModel
from app.config import get_settings


@lru_cache
def get_client():
    settings = get_settings()
    if not settings.enable_llm or not settings.azure_openai_api_key:
        raise RuntimeError('Azure OpenAI is not configured; set AZURE_OPENAI_API_KEY or disable LLM')
    return OpenAI(base_url=settings.azure_base_url, api_key=settings.azure_openai_api_key, timeout=60.0, max_retries=2)


def structured(system: str, prompt: str, schema: type[BaseModel]):
    result = get_client().responses.parse(
        model=get_settings().azure_openai_deployment,
        instructions=system,
        input=prompt,
        text_format=schema,
        store=False,
    )
    if result.output_parsed is None:
        raise RuntimeError('Azure OpenAI returned no structured output')
    return result.output_parsed


def generate(system: str, prompt: str) -> str:
    result = get_client().responses.create(
        model=get_settings().azure_openai_deployment,
        instructions=system,
        input=prompt,
        store=False,
    )
    return result.output_text or ''
