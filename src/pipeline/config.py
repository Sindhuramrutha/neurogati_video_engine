"""Environment configuration, read in exactly one place.

Same pattern as v1's config/settings.py, which was good design and survived a real
provider migration as a config change -- typed here rather than hand-parsed.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- LLM: text (comprehension, briefs) ---
    llm_base_url: str = "https://api.tokenrouter.com/v1"
    llm_api_key: str = "not-needed"
    llm_model: str = "deepseek/deepseek-v4-flash"

    # --- LLM: structured/IR generation. Falls back to the text model if unset. ---
    ir_llm_base_url: str | None = None
    ir_llm_api_key: str | None = None
    ir_llm_model: str | None = None

    # --- Images: drawing a replacement for a figure that did not extract ---
    # The same provider and key as the text model unless told otherwise, because
    # the OpenAI-compatible endpoints that serve one usually serve both.
    image_base_url: str | None = None
    image_api_key: str | None = None
    image_model: str = "google/gemini-2.5-flash-image"

    # Explicit, unlike v1 -- see docs/decisions/0003-durable-incremental-state.md.
    # A dropped connection there surfaced as a failed scene with no code generated,
    # losing minutes of work per scene.
    llm_timeout_seconds: float = 600.0
    llm_max_retries: int = 3

    tts_voice: str = "af_heart"

    # --- storage: files are the source of truth (ADR 0005) ---
    projects_dir: Path = REPO_ROOT / "projects"

    @property
    def ir_llm(self) -> tuple[str, str, str]:
        """(base_url, api_key, model) for IR generation, falling back to the text model."""
        return (
            self.ir_llm_base_url or self.llm_base_url,
            self.ir_llm_api_key or self.llm_api_key,
            self.ir_llm_model or self.llm_model,
        )

    @property
    def image_llm(self) -> tuple[str, str, str]:
        """(base_url, api_key, model) for drawing pictures."""
        return (
            self.image_base_url or self.llm_base_url,
            self.image_api_key or self.llm_api_key,
            self.image_model,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
