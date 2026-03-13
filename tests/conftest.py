"""Shared pytest fixtures for Coursera MCP tests."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from coursera_mcp.client import CourseraClient
from coursera_mcp.config import CourseraConfig


@pytest.fixture
def config() -> CourseraConfig:
    return CourseraConfig(cauth=None)


@pytest.fixture
def auth_config() -> CourseraConfig:
    return CourseraConfig(cauth="test_cauth_token")


@pytest.fixture
def mock_client(config: CourseraConfig) -> CourseraClient:
    """A CourseraClient whose HTTP methods are replaced with AsyncMocks."""
    client = CourseraClient(config)
    client.get = AsyncMock()  # type: ignore[method-assign]
    return client
