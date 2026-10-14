"""Environment configuration, read in exactly one place.

Typed settings rather than hand-parsed variables, so changing provider is a
configuration change.
"""

from __future__ import annotations

import os
import tempfile
from functools import lru_cache
from pathlib import Path

from pydantic import Field
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

    # --- Vision: the Extraction agent looking at slides, and handwriting OCR ---
    # The text model cannot see a picture, so this is a separate, multimodal one --
    # one the provider actually offers: TokenRouter has no channel for 2.5-flash.
    vision_base_url: str | None = None
    vision_api_key: str | None = None
    vision_model: str = "google/gemini-3.5-flash"

    # Explicit: a dropped connection otherwise surfaces as a failed scene with no
    # code generated, losing minutes of work per scene.
    llm_timeout_seconds: float = 600.0
    llm_max_retries: int = 3

    # --- storage: files are the source of truth ---
    projects_dir: Path = REPO_ROOT / "projects"
    # Working files on the project's drive, not the system temp folder: the system
    # drive filled up and took memory with it (Windows grows its page file there).
    work_dir: Path = Field(REPO_ROOT / ".cache" / "tmp", validation_alias="PIPELINE_TEMP")

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

    @property
    def vision_llm(self) -> tuple[str, str, str]:
        """(base_url, api_key, model) for reading text out of a page image."""
        return (
            self.vision_base_url or self.llm_base_url,
            self.vision_api_key or self.llm_api_key,
            self.vision_model,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def use_work_dir() -> None:
    """Point this process and everything it starts at the working-files folder.
    Called by every entry point: the CLI, the web app and the MCP server."""
    folder = get_settings().work_dir
    folder.mkdir(parents=True, exist_ok=True)
    for name in ("TMP", "TEMP", "TMPDIR"):
        os.environ[name] = str(folder)
    tempfile.tempdir = str(folder)
