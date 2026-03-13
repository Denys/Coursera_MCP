"""Configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

BASE_URL = "https://api.coursera.org/api"


@dataclass(frozen=True)
class CourseraConfig:
    """Configuration for the Coursera MCP server.

    The Catalog API is publicly accessible without authentication.
    A CAUTH token enables access to enrolled course content.
    """

    cauth: str | None
    base_url: str = field(default=BASE_URL)

    @property
    def has_auth(self) -> bool:
        return bool(self.cauth)


def load_config() -> CourseraConfig:
    """Load configuration from environment variables."""
    return CourseraConfig(
        cauth=os.environ.get("COURSERA_CAUTH") or None,
    )
