"""Tests for search tools."""

from __future__ import annotations

import json

import pytest

from coursera_mcp.tools.search import search_courses


@pytest.mark.asyncio
async def test_search_courses(mock_client):
    mock_client.get.return_value = {
        "elements": [
            {"id": "abc", "slug": "ml", "name": "Machine Learning"},
            {"id": "def", "slug": "dl", "name": "Deep Learning"},
        ],
        "paging": {"total": 2},
    }
    result = await search_courses(mock_client, query="learning")
    data = json.loads(result)
    assert data["total"] == 2
    assert len(data["courses"]) == 2


@pytest.mark.asyncio
async def test_search_courses_empty(mock_client):
    mock_client.get.return_value = {"elements": [], "paging": {"total": 0}}
    result = await search_courses(mock_client, query="zzzznonexistent")
    data = json.loads(result)
    assert data["total"] == 0
    assert data["courses"] == []


@pytest.mark.asyncio
async def test_search_courses_pagination(mock_client):
    mock_client.get.return_value = {
        "elements": [{"id": "ghi", "slug": "stats", "name": "Statistics"}],
        "paging": {"total": 50},
    }
    result = await search_courses(mock_client, query="statistics", start=10, limit=1)
    data = json.loads(result)
    assert data["total"] == 50
    mock_client.get.assert_called_once()
    call_kwargs = mock_client.get.call_args
    assert call_kwargs.kwargs.get("start") == 10 or call_kwargs[1].get("start") == 10
