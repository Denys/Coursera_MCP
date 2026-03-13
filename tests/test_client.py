"""Tests for CourseraClient."""

from __future__ import annotations

import pytest

from coursera_mcp.client import CourseraClient, CourseraError
from coursera_mcp.config import CourseraConfig


@pytest.mark.asyncio
async def test_get_success(httpx_mock):
    config = CourseraConfig(cauth=None)
    httpx_mock.add_response(
        json={"elements": [{"id": "abc", "name": "Test Course"}], "paging": {"total": 1}},
    )
    client = CourseraClient(config)
    data = await client.get("catalog.v1/courses", limit=1)
    assert data["elements"][0]["name"] == "Test Course"
    await client.aclose()


@pytest.mark.asyncio
async def test_get_raises_on_error(httpx_mock):
    config = CourseraConfig(cauth=None)
    httpx_mock.add_response(status_code=404, text="Not Found")
    client = CourseraClient(config)
    with pytest.raises(CourseraError) as exc_info:
        await client.get("catalog.v1/courses/nonexistent")
    assert exc_info.value.status_code == 404
    await client.aclose()


@pytest.mark.asyncio
async def test_get_with_cauth_cookie(httpx_mock):
    config = CourseraConfig(cauth="my_cauth")
    httpx_mock.add_response(
        json={"elements": [], "paging": {"total": 0}},
    )
    client = CourseraClient(config)
    await client.get("catalog.v1/courses")
    request = httpx_mock.get_request()
    assert "CAUTH" in str(request.headers.get("cookie", ""))
    await client.aclose()
